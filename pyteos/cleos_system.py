#!/usr/bin/python3

"""
Python front-end for `EOSIO cleos system`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos system`.

.. moduleauthor:: Tokenika

"""

import setup
import cleos

def reload():
    import importlib
    importlib.reload(cleos)

setup_setup = setup.Setup()


class SystemNewaccount(cleos._Cleos):
    """ Create an account, buy ram, stake for bandwidth for the account.

    - **parameters**::

        creator: The name, of the account creating the new account. May be an 
            object having the attribute `name`, like `CreateAccount`, 
            or a string.
        name: The name of the new account.
        owner_key: The owner public key for the new account.
        active_key: The active public key for the new account.
        stake_net: The amount of EOS delegated for net bandwidth.
        stake_cpu: The amount of EOS delegated for CPU bandwidth.
        buy_ram: The amount of RAM bytes to purchase for the new account in EOS.
        transfer: Transfer voting power and right to unstake EOS to receiver.
        permission: An account and permission level to authorize, as in 
            'account@permission'. May be a `CreateAccount` or `Account` object
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).

    - **attributes**::

        owner_key: Owner private key.
        active_key: Active private key.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the constraction time.
    """
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu,
            permission = "",
            buy_ram_kbytes = 0, buy_ram = "",
            transfer = False,
            expiration_sec = 30, 
            skip_signature = 0, dont_broadcast = 0, forceUnique = 0,
            max_cpu_usage = 0, max_net_usage = 0,
            ref_block = "",
            is_verbose = 1
            ):
        try:
            creator_name = creator.name
        except:
            creator_name = creator

        self.owner_key = None # private keys
        self.active_key = None
        
        try:
            owner_key_public = owner_key.key_public
            self.owner_key = owner_key.key_private
        except:
            owner_key_public = owner_key

        if not active_key:
            active_key = owner_key

        try:
            active_key_public = active_key.key_public
            self.active_key = active_key.key_private
        except:
            active_key_public = active_key

        args = [creator_name, name, owner_key_public, active_key_public]
        if setup.is_json():
            args.append("--json")
        args.extend(["--stake-net", stake_net, "--stake-cpu", stake_cpu])
        if buy_ram_kbytes:
            args.extend(["--buy-ram-kbytes", str(buy_ram_kbytes)])
        if buy_ram:
            args.extend(["buy-ram", buy_ram])
        if transfer:
            args.extend(["--transfer"])
        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission

            args.extend(["--permission", permission_name])
        if skip_signature:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if forceUnique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", max_cpu_usage])
        if  max_net_usage:
            args.extend(["--max-net-usage", max_net_usage])
        if  ref_block:
            args.extend(["--ref-block", ref_block])

        self.name = name

        cleos._Cleos.__init__(
            self, args, "system", "newaccount", is_verbose)
            
        if not self.error and setup.is_json():
            self.json = cleos.GetAccount(
                self.name, is_verbose=0, json=True).json

            if self.is_verbose:
                print(self.__str__())

    def info(self):
        return str(cleos.GetAccount(self.name, is_verbose=1))
            
    def __str__(self):
        return self.name