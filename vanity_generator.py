from nacl.signing import SigningKey
import hashlib
import multiprocessing as mp
import time


# Modify this number to change the number of 0s at the beginning of the address
TARGET_ZEROS = 5


class Account:
    """Represents an account as well as the private, public key-pair for the Aptos blockchain."""

    def __init__(self) -> None:
        self.signing_key = SigningKey.generate()

    def address(self) -> str:
        """Returns the address associated with the given account"""

        return self.auth_key()[-32:]

    def auth_key(self) -> str:
        """Returns the auth_key for the associated account"""

        hasher = hashlib.sha3_256()
        hasher.update(self.signing_key.verify_key.encode() + b'\x00')
        return hasher.hexdigest()

    def priv_key(self) -> str:
        """Returns the public key for the associated account"""

        return self.signing_key._seed.hex()


def gen_addresses() -> str:
    while True:
        temp = Account()
        address = temp.address()
        if address[:TARGET_ZEROS] == "0" * TARGET_ZEROS:
            print(f"Address: {address}")
            print(f"Private key: {temp.priv_key()}")
            return temp.priv_key()


def callback(_):
    pool.terminate()


if __name__ == "__main__":
    start_time = time.time()
    cpus = mp.cpu_count()

    pool = mp.Pool()
    multiple_results = [pool.apply_async(gen_addresses, (), callback=callback) for _ in range(cpus)]
    pool.close()
    pool.join()
    print(f"Address found in {round(time.time()-start_time, 2)} seconds")
