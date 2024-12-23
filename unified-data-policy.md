# Unified data policy

## Replication policies

- Level 4: at least 4 copies, in 3 location, 2 countries, 2 continents. 

- Level 3: at least 3 copies, in 2 location, 2 countries. 

- Level 2: at least 2 copies. 

- Level 1: at least 1 copies. 

## Confidential Policies

> `sensitive` means I don't want to leak it, `important` means I don't want to lost it. 

- type I2: non-sensitive important data, such as environent setup script, software installation packs, saved movies.

- type I: public personal data, or non-important public data.

- type C2: sensitive important personal data, such as photos, game save, server data.

- type C: sensitive non-important personal data, such as system logs, chat logs, screenshots, web history, development environment.

- type M: secret keys/seeds/passwords, banking account/card information.

- type MX: GPG masterkey itself. 

- [TODO]X

> **super key doesn't not apply any data policy, only allowed to store in-brain.** 

|Type|Encryption|Ownership|Replication|Current\_Solution|
|---|---|---|---|---|
|MX|Always, by cold key and super key|1P|Level 4|nfs/backup/MX|
|M|Always, by GPG master key or super key|1P|Level 4|nfs/backup/C2_M|
|C2|Only on untrusted device|1P / 3P|Level 3|nfs/backup/C2_M, RecoDrive|
|C|Device-level encryption|1P / 3P|Level 1|any encrypted devices|
|I2|Optional|1P / 3P|Level 2|nfs/backup/I2, RecoGit, RecoDrive|
|I|Optional|1P / 3P|Level 1|any devices|

|Properties|Important|Non-Important|
|---|---|---|
|Sensitive|MX,M,C2|C|
|Non-sensitive|I2|I|

![](./.res/reco-file-types.png)

All device storing / processing unencrypted sensitive data, must either using Fully-Open-Source-Software, or be disconnected from Internet and destroyed afterward. 
