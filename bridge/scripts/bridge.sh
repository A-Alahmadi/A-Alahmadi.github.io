#!/usr/bin/env bash
# bridge.sh: جسر بين Claude Code وشات جي بي تي (Codex CLI) عبر stdin.
# الاستخدام:
#   bridge.sh selftest                 فحص التثبيت وتسجيل الدخول والاتصال
#   bridge.sh ask "نص"                 سؤال جديد، وضع قراءة فقط
#   bridge.sh ask - < ملف              نفس الشيء من ملف
#   bridge.sh continue "نص"            متابعة آخر جلسة (resume --last) مع تمرير الخلاصة
#   bridge.sh write "نص"               مهمة تنفيذية بصلاحية كتابة، تتطلب BRIDGE_ALLOW_WRITE=1
#   bridge.sh log                      آخر 40 سطراً من السجل
set -u -o pipefail
CMD="${1:-help}"; shift || true
ROOT="${BRIDGE_ROOT:-$PWD}"
DIR="$ROOT/.bridge"; mkdir -p "$DIR"
LOG="$DIR/transcript.md"; LAST="$DIR/last.md"
MODEL_ARGS=(); [ -n "${BRIDGE_MODEL:-}" ] && MODEL_ARGS=(-m "$BRIDGE_MODEL")
COMMON=(--skip-git-repo-check --color never -C "$ROOT" -o "$LAST")

stamp(){ date +"%Y-%m-%d %H:%M"; }
say(){ printf '%s\n' "$*"; }
need_codex(){ command -v codex >/dev/null 2>&1 || { say "[ كلود ] Codex غير مثبّت. ثبّته: npm i -g @openai/codex"; exit 2; }; }
read_input(){ if [ "${1:-}" = "-" ] || [ $# -eq 0 ]; then cat; else printf '%s' "$*"; fi; }
append_log(){ { printf '\n### %s · %s\n\n' "$1" "$(stamp)"; cat; printf '\n'; } >> "$LOG"; }
context_tail(){ [ -f "$LOG" ] && tail -n 60 "$LOG" || true; }

run_codex(){ # $1 sandbox, stdin = prompt
  local sb="$1"; shift
  codex exec "${COMMON[@]}" "${MODEL_ARGS[@]}" --sandbox "$sb" "$@" - 2>"$DIR/stderr.log"
  local rc=$?
  if [ $rc -ne 0 ]; then
    say "[ كلود ] فشل أمر الشريك (rc=$rc). آخر سطور الخطأ:"; tail -n 5 "$DIR/stderr.log" || true
    say "[ كلود ] أكمل بمفردي ولا أختلق رداً باسمه."
  fi
  return $rc
}

case "$CMD" in
  selftest)
    need_codex
    say "[ كلود ] الإصدار: $(codex --version 2>&1 | head -1)"
    if codex login status >/dev/null 2>&1; then say "[ كلود ] تسجيل الدخول: موجود"; else say "[ كلود ] تسجيل الدخول: غير موجود. نفّذ: codex login"; exit 3; fi
    out="$(printf 'ردّ بكلمة واحدة فقط: جاهز' | codex exec "${COMMON[@]}" --sandbox read-only --ephemeral - 2>"$DIR/stderr.log")" || { say "[ كلود ] اختبار الاتصال فشل:"; tail -n 3 "$DIR/stderr.log"; exit 4; }
    say "[ شات جي بي تي ] $out"
    say "[ القرار المشترك ] الجسر جاهز. أعطني أول مهمة."
    ;;
  ask)
    need_codex
    prompt="$(read_input "$@")"
    printf '%s' "$prompt" | append_log "[ كلود ] إلى الشريك"
    printf '%s' "$prompt" | run_codex read-only | tee >(append_log "[ شات جي بي تي ]")
    ;;
  continue)
    need_codex
    prompt="$(read_input "$@")"
    printf '%s' "$prompt" | append_log "[ كلود ] متابعة"
    if ! printf '%s' "$prompt" | codex exec resume --last "${COMMON[@]}" --sandbox read-only - 2>"$DIR/stderr.log" | tee >(append_log "[ شات جي بي تي ]"); then
      say "[ كلود ] resume غير متاح، أعيد الإرسال مع خلاصة السجل."
      { say "خلاصة الحوار السابق:"; context_tail; say ""; say "الطلب الحالي:"; printf '%s\n' "$prompt"; } | run_codex read-only | tee >(append_log "[ شات جي بي تي ]")
    fi
    ;;
  write)
    need_codex
    [ "${BRIDGE_ALLOW_WRITE:-0}" = "1" ] || { say "[ كلود ] صلاحية الكتابة مقفلة. تحتاج إذن أحمد الصريح ثم: BRIDGE_ALLOW_WRITE=1 bridge.sh write ..."; exit 5; }
    prompt="$(read_input "$@")"
    printf '%s' "$prompt" | append_log "[ كلود ] مهمة تنفيذية للشريك (workspace-write)"
    printf '%s' "$prompt" | run_codex workspace-write | tee >(append_log "[ شات جي بي تي ] تنفيذ")
    ;;
  log) [ -f "$LOG" ] && tail -n 40 "$LOG" || say "لا يوجد سجل بعد." ;;
  *) sed -n '2,10p' "$0" ;;
esac
