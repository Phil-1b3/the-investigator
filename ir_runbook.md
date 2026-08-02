# Ransomware Incident Response Runbook

## 1. Preparation

1. [ ] Confirm incident-response roles, contacts, and escalation paths.
2. [ ] Ensure backups are identified, tested, and protected from encryption.
3. [ ] Verify logging, endpoint detection, and alerting are enabled.
4. [ ] Prepare communications for staff, leadership, legal, and external partners.
5. [ ] Document approved containment, eradication, and recovery actions in advance.

## 2. Detection & Analysis

1. [ ] Confirm the incident is truly ransomware by checking for ransom notes, mass file encryption, and changed file extensions.
2. [ ] Determine the blast radius: affected hosts, users, accounts, and data.
3. [ ] Preserve evidence before changing anything: capture volatile data first, including memory, active connections, and logged-in users.
4. [ ] Collect the relevant logs and correlate authentication, network, and file activity.
5. [ ] Do not power off encrypted machines; preserve them for analysis where possible.
6. [ ] Record indicators of compromise, including IPs, domains, hashes, ransom notes, and malware names.

## 3. Containment, Eradication & Recovery

1. [ ] Isolate affected hosts from the network to stop spread.
2. [ ] Disable compromised accounts and reset credentials where appropriate.
3. [ ] Block known malicious IPs, domains, and malware indicators at network controls.
4. [ ] Preserve forensic evidence before making major changes.
5. [ ] Remove malware, rebuild or reimage impacted systems, and restore from known-good backups.
6. [ ] Restore only from offline or verified-clean backups; do not rely on decryption tools as a first resort.
7. [ ] Monitor for persistence, reactivation, or repeat encryption activity.

## 4. Post-Incident

1. [ ] Document the full timeline, every action taken, and all indicators of compromise.
2. [ ] Map the observed activity to MITRE ATT&CK techniques such as T1110, T1071, and T1486.
3. [ ] Hold a lessons-learned review and fix the root cause, including the entry vector.
4. [ ] Tune detections, improve defenses, and update this runbook.
5. [ ] Make any required notifications to legal, regulators, or affected parties according to policy.
