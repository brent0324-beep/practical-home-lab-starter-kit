# labctl five-minute-lab demo tape
# Render on BAILAB (needs Docker + containerlab + clab_admins active):
#   cd /opt/products/practical-home-lab-starter-kit
#   vhs demo/labctl-two-node.tape
# Produces demo/labctl-two-node.gif
#
# Prereqs before rendering:
#   - a fresh login session so clab_admins is active (NOT a newgrp subshell,
#     or the recorded prompt/behavior won't match a real user's)
#   - no stale `clab` docker network with a conflicting subnet
#     (docker network rm clab  if a previous lab left one)
#   - the two-node lab NOT already deployed

Output demo/labctl-two-node.gif

# --- terminal appearance ---
Set Shell "bash"
Set FontSize 16
Set Width 1100
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 45ms

# --- start clean ---
Type "cd /opt/products/practical-home-lab-starter-kit"
Enter
Sleep 800ms
Type "clear"
Enter
Sleep 500ms

# --- 1. show the spec (the whole point: one small file) ---
Type "cat labs/examples/two-node-point-to-point/lab.yaml"
Enter
Sleep 3s

# --- 2. deploy ---
Type "./scripts/labctl deploy labs/examples/two-node-point-to-point/lab.yaml --profile profiles/labs/two-node-ptp-fast.yaml"
Enter
Sleep 8s

# --- 3. status: two nodes running ---
Type "./scripts/labctl status two-node-ptp"
Enter
Sleep 4s

# --- 4. prove the link works ---
Type "docker exec -it clab-two-node-ptp-router-a ping -c 3 172.30.90.112"
Enter
Sleep 5s

# --- 5. scoped teardown ---
Type "./scripts/labctl destroy two-node-ptp"
Enter
Sleep 5s

# --- 6. nothing left behind ---
Type "docker ps -a --filter label=io.labctl.managed=true"
Enter
Sleep 3s

# hold the final frame so the GIF loop has a readable pause
Sleep 2s
