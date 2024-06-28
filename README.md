## Scrapbook repo for testing and learning inventory plugins

PoC to see how the ansible helper functions ease dynamic inventory creation.

Path defaults added to ansible.cfg, data in local directory.

Example usage:

```
$ ansible-inventory -i inventory/event_hub.yml --list
{
    "MSFT SQL Instance": {
        "hosts": [
            "Server050002066",
            "Server050002067",
            "Server050002068",
            "Server050002069"
        ]
    },
    "_meta": {
        "hostvars": {
            "Server050002066": {
                "database": "Server050002066\\SRA_SQLVIRT_DEV - sharpe_ref1"
            },
            "Server050002067": {
                "database": "Server050002067\\SRA_SQLVIRT_DEV - sharpe_ref2"
            },
            "Server050002068": {
                "database": "Server050002068\\SRA_SQLVIRT_DEV - sharpe_ref1"
            },
            "Server050002069": {
                "database": "Server050002069\\SRA_SQLVIRT_DEV - sharpe_ref2"
            }
        }
    },
    "all": {
        "children": [
            "MSFT SQL Instance",
            "ungrouped"
        ]
    }
}
```
