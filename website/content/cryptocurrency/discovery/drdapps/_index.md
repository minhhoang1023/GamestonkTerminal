```
usage: drdapps [-l N] [-s {Name,Category,Protocols,Daily Users,Daily Volume [$]}] [--descend] [-l] [--export {csv,json,xlsx}] [-h]
```

Shows top decentralized applications [Source: https://dappradar.com/]

Accepts --sort {Name,Category,Protocols,Daily Users,Daily Volume [$]} to sort by column

```
optional arguments:
  -l N, --limit N       display N records (default: 15)
  -s --sort {Name,Category,Protocols,Daily Users,Daily Volume [$]}
                        Sort by given column
  --export {csv,json,xlsx}
                        Export dataframe data to csv,json,xlsx file (default: )
  -h, --help            show this help message (default: False)
```
