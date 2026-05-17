<#
  vpn-control.ps1 — demand-driven VPN connect/disconnect for sources-fetch Method D.

  Called by framework/building-blocks/sources-fetch.md (Method D pre-flight and
  post-fetch teardown) and by the optional .claude/settings.json SessionEnd hook.

  Contains NO credentials. It only ever takes a vpncli.exe path and a VPN profile
  NAME as arguments; authentication is handled entirely by the Cisco client's own
  saved profile / Windows credential store (cert or saved creds, no MFA).

  Ownership model: a per-user marker file in %TEMP% records that *we* brought the
  tunnel up. disconnect only acts when that marker exists, so a tunnel the user
  opened themselves is never torn down, and the SessionEnd hook is a pure no-op
  unless we left a tunnel up.

  IT blocks vpncli.exe? Point -VpnCli at an openconnect wrapper that honours the
  same status|connect|disconnect verbs and the exit-code contract below.

  Exit codes
    status:      0 connected | 3 disconnected | 4 vpncli not found / unparseable
    connect:     0 we connected (marker written) | 2 pre-existing tunnel (no marker)
                 4 vpncli missing | 5 connect failed/timed out | 6 bad args
    disconnect:  0 disconnected or clean no-op | 5 disconnect failed (marker kept)
                 7 vpncli missing (marker deleted anyway)
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('status', 'connect', 'disconnect')]
    [string]$Action,

    [string]$VpnCli,
    [string]$Profile,
    [int]$TimeoutSec = 45
)

$ErrorActionPreference = 'Stop'
$MarkerPath = Join-Path $env:TEMP 'mpf-vpn-owned.marker'

function Resolve-VpnCli {
    if ($VpnCli -and (Test-Path -LiteralPath $VpnCli)) { return $VpnCli }
    $candidates = @(
        "${env:ProgramFiles(x86)}\Cisco\Cisco Secure Client\vpncli.exe",
        "${env:ProgramFiles(x86)}\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe",
        "$env:ProgramFiles\Cisco\Cisco Secure Client\vpncli.exe",
        "$env:ProgramFiles\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe"
    )
    foreach ($c in $candidates) { if ($c -and (Test-Path -LiteralPath $c)) { return $c } }
    $onPath = Get-Command 'vpncli.exe' -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }
    return $null
}

function Get-State {
    param([string]$Cli)
    # `vpncli.exe state` prints one or more "  >> state: <Word>" lines.
    # Take the last state token; permissive so client-version wording variations
    # still parse. Anything unrecognised -> UNKNOWN (caller decides).
    try {
        $raw = & $Cli state 2>&1 | Out-String
    } catch {
        return 'UNKNOWN'
    }
    $matches = [regex]::Matches($raw, '(?im)state:\s*([A-Za-z]+)')
    if ($matches.Count -eq 0) { return 'UNKNOWN' }
    $last = $matches[$matches.Count - 1].Groups[1].Value
    switch -Regex ($last) {
        '^(?i)Connected$'    { return 'CONNECTED' }
        '^(?i)Disconnected$' { return 'DISCONNECTED' }
        default              { return 'UNKNOWN' }   # Connecting / Reconnecting / etc.
    }
}

function Write-Marker {
    param([string]$ProfileName)
    $obj = [ordered]@{
        owned_by      = 'mpf-vpn-control'
        profile       = $ProfileName
        connected_utc = (Get-Date).ToUniversalTime().ToString('o')
        pid           = $PID
    }
    ($obj | ConvertTo-Json -Compress) | Set-Content -LiteralPath $MarkerPath -NoNewline -Encoding UTF8
}

$cli = Resolve-VpnCli

switch ($Action) {

    'status' {
        if (-not $cli) { 'UNKNOWN'; exit 4 }
        $s = Get-State -Cli $cli
        $s
        if ($s -eq 'CONNECTED')        { exit 0 }
        elseif ($s -eq 'DISCONNECTED') { exit 3 }
        else                           { exit 4 }
    }

    'connect' {
        if (-not $cli)               { Write-Error 'vpncli.exe not found'; exit 4 }
        if (-not $Profile)           { Write-Error 'connect requires -Profile'; exit 6 }
        # Never adopt-then-own a tunnel the user opened: decide ownership from
        # live state BEFORE we touch anything.
        if ((Get-State -Cli $cli) -eq 'CONNECTED') { exit 2 }
        try {
            # Close stdin ($null) so an unexpected prompt hits EOF instead of
            # hanging; saved-creds/cert profiles need no interaction.
            $null | & $cli connect $Profile 2>&1 | Out-Null
        } catch {
            exit 5
        }
        $deadline = (Get-Date).AddSeconds($TimeoutSec)
        do {
            Start-Sleep -Seconds 2
            $state = Get-State -Cli $cli
        } until ($state -eq 'CONNECTED' -or (Get-Date) -gt $deadline)
        if ($state -ne 'CONNECTED') { exit 5 }
        try { Write-Marker -ProfileName $Profile } catch { exit 5 }
        exit 0
    }

    'disconnect' {
        # Marker absent => we don't own a tunnel => nothing of ours to do.
        if (-not (Test-Path -LiteralPath $MarkerPath)) { exit 0 }
        if (-not $cli) {
            # Can't drive the client, but clear our ownership record so we don't
            # get stuck believing we own a tunnel forever.
            Remove-Item -LiteralPath $MarkerPath -Force -ErrorAction SilentlyContinue
            exit 7
        }
        # Stale marker but tunnel already down (user/OS dropped it): just clear.
        if ((Get-State -Cli $cli) -ne 'DISCONNECTED') {
            try {
                & $cli disconnect 2>&1 | Out-Null
            } catch {
                exit 5   # keep the marker so a later run / SessionEnd hook retries
            }
            if ((Get-State -Cli $cli) -ne 'DISCONNECTED') { exit 5 }
        }
        Remove-Item -LiteralPath $MarkerPath -Force -ErrorAction SilentlyContinue
        exit 0
    }
}
