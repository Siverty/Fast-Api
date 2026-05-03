#!/usr/bin/env bash
# Generate_logs.sh — produces copious amounts of log output
# Currently used to get logs back trough FastAPI
 
# ── Config ────────────────────────────────────────────────────────────────────
LOG_FILE="${1:-app.log}"          
LOG_LEVELS=(DEBUG INFO INFO INFO WARN ERROR) 
COMPONENTS=(database api cache scheduler worker auth gateway)
MESSAGES=(
  "Starting process"
  "Initialised connection pool"
  "Request received"
  "Processing payload"
  "Cache miss — fetching from source"
  "Cache hit"
  "Query executed in ${RANDOM}ms"
  "Response dispatched"
  "Retrying after transient failure"
  "Health check passed"
  "Threshold exceeded, backing off"
  "Token refreshed"
  "Session validated"
  "Record inserted"
  "Record updated"
  "Batch complete"
  "Checkpoint written"
  "Config reloaded"
  "Connection closed gracefully"
  "Unexpected null value encountered"
)
 
# ── Helpers ───────────────────────────────────────────────────────────────────
timestamp()  { date '+%Y-%m-%dT%H:%M:%S.%3N'; }
rand_item()  { local arr=("$@"); echo "${arr[RANDOM % ${#arr[@]}]}"; }
rand_int()   { echo $(( RANDOM % ($2 - $1 + 1) + $1 )); }
pad()        { printf "%-7s" "$1"; }
 
log_line() {
  local level component message request_id latency
  level="$(rand_item "${LOG_LEVELS[@]}")"
  component="$(rand_item "${COMPONENTS[@]}")"
  message="$(rand_item "${MESSAGES[@]}")"
  request_id="$(printf '%08x' $RANDOM$RANDOM)"
  latency="$(rand_int 1 450)"
 
  printf '%s  %s  [%-9s]  req=%s  latency=%dms  %s\n' \
    "$(timestamp)" "$(pad "$level")" "$component" \
    "$request_id" "$latency" "$message"
}
 
# ── Main ──────────────────────────────────────────────────────────────────────
ITERATIONS="${2:-500}"
BURST_SIZE="${3:-20}"
 
echo "Writing $ITERATIONS log lines to: $LOG_FILE"
echo "─────────────────────────────────────────────"
 
> "$LOG_FILE"   # truncate / create
 
written=0
while (( written < ITERATIONS )); do
  # write a burst
  burst=$(( BURST_SIZE < (ITERATIONS - written) ? BURST_SIZE : (ITERATIONS - written) ))
  for (( i=0; i<burst; i++ )); do
    log_line | tee -a "$LOG_FILE"
    (( written++ ))
  done
  sleep 0.05
done
 
echo "─────────────────────────────────────────────"
echo "Done. $written lines written to $LOG_FILE"
echo "File size: $(du -h "$LOG_FILE" | cut -f1)"
echo "File location: $(realpath "$LOG_FILE")"
 
