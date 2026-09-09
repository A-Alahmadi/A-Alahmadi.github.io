<#
bridge.ps1: جسر بين Claude Code وشات جي بي تي (Codex CLI) على ويندوز.
  .\bridge.ps1 selftest
  .\bridge.ps1 ask "نص"           |  Get-Content q.txt -Raw | .\bridge.ps1 ask -
  .\bridge.ps1 continue "نص"
  $env:BRIDGE_ALLOW_WRITE=1; .\bridge.ps1 write "نص"
  .\bridge.ps1 log
#>
param([Parameter(Position=0)][string]$Cmd = "help", [Parameter(Position=1, ValueFromRemainingArguments=$true)][string[]]$Rest)
$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = $utf8; [Console]::OutputEncoding = $utf8; $OutputEncoding = $utf8
$Root = if ($env:BRIDGE_ROOT) { $env:BRIDGE_ROOT } else { (Get-Location).Path }
$Dir = Join-Path $Root ".bridge"; New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$Log = Join-Path $Dir "transcript.md"; $Last = Join-Path $Dir "last.md"; $Err = Join-Path $Dir "stderr.log"
$Common = @("--skip-git-repo-check","--color","never","-C",$Root,"-o",$Last)
if ($env:BRIDGE_MODEL) { $Common += @("-m",$env:BRIDGE_MODEL) }

function Say($t) { Write-Host $t }
function Need-Codex { if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { Say "[ كلود ] Codex غير مثبّت. ثبّته: npm i -g @openai/codex"; exit 2 } }
function Read-Input($r) { if (-not $r -or $r[0] -eq "-") { [Console]::In.ReadToEnd() } else { ($r -join " ") } }
function Append-Log($who, $text) { Add-Content -Path $Log -Encoding UTF8 -Value ("`n### {0} · {1}`n`n{2}`n" -f $who, (Get-Date -Format "yyyy-MM-dd HH:mm"), $text) }
function Run-Codex($sandbox, $prompt, [string[]]$extra = @()) {
  $out = ($prompt | & codex exec @Common @extra --sandbox $sandbox - 2>$Err) -join "`n"
  if ($LASTEXITCODE -ne 0) {
    Say "[ كلود ] فشل أمر الشريك (rc=$LASTEXITCODE). آخر سطور الخطأ:"; if (Test-Path $Err) { Get-Content $Err -Tail 5 }
    Say "[ كلود ] أكمل بمفردي ولا أختلق رداً باسمه."; return $null
  }
  return $out
}

switch ($Cmd) {
  "selftest" {
    Need-Codex
    Say ("[ كلود ] الإصدار: " + ((& codex --version 2>&1) | Select-Object -First 1))
    & codex login status *> $null
    if ($LASTEXITCODE -ne 0) { Say "[ كلود ] تسجيل الدخول: غير موجود. نفّذ: codex login"; exit 3 } else { Say "[ كلود ] تسجيل الدخول: موجود" }
    $out = Run-Codex "read-only" "ردّ بكلمة واحدة فقط: جاهز" @("--ephemeral")
    if ($null -eq $out) { exit 4 }
    Say "[ شات جي بي تي ] $out"; Say "[ القرار المشترك ] الجسر جاهز. أعطني أول مهمة."
  }
  "ask" { Need-Codex; $p = Read-Input $Rest; Append-Log "[ كلود ] إلى الشريك" $p; $o = Run-Codex "read-only" $p; if ($o) { Say $o; Append-Log "[ شات جي بي تي ]" $o } }
  "continue" {
    Need-Codex; $p = Read-Input $Rest; Append-Log "[ كلود ] متابعة" $p
    $o = ($p | & codex exec resume --last @Common --sandbox read-only - 2>$Err) -join "`n"
    if ($LASTEXITCODE -ne 0) {
      Say "[ كلود ] resume غير متاح، أعيد الإرسال مع خلاصة السجل."
      $ctx = if (Test-Path $Log) { (Get-Content $Log -Tail 60) -join "`n" } else { "" }
      $o = Run-Codex "read-only" ("خلاصة الحوار السابق:`n$ctx`n`nالطلب الحالي:`n$p")
    }
    if ($o) { Say $o; Append-Log "[ شات جي بي تي ]" $o }
  }
  "write" {
    Need-Codex
    if ($env:BRIDGE_ALLOW_WRITE -ne "1") { Say "[ كلود ] صلاحية الكتابة مقفلة. تحتاج إذن أحمد الصريح ثم: `$env:BRIDGE_ALLOW_WRITE=1"; exit 5 }
    $p = Read-Input $Rest; Append-Log "[ كلود ] مهمة تنفيذية للشريك (workspace-write)" $p
    $o = Run-Codex "workspace-write" $p; if ($o) { Say $o; Append-Log "[ شات جي بي تي ] تنفيذ" $o }
  }
  "log" { if (Test-Path $Log) { Get-Content $Log -Tail 40 } else { Say "لا يوجد سجل بعد." } }
  default { Get-Content $PSCommandPath -TotalCount 9 | Select-Object -Skip 1 }
}
