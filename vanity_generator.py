from nacl.signing import SigningKey
import argparse
import hashlib
import multiprocessing as mp
import time


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
        hasher.update(self.signing_key.verify_key.encode() + b"\x00")
        return hasher.hexdigest()

    def priv_key(self) -> str:
        """Returns the public key for the associated account"""

        return self.signing_key._seed.hex()


def gen_addresses(num_zeros: int) -> str:
    while True:
        temp = Account()
        address = temp.address()
        if address[:num_zeros] == "0" * num_zeros:
            print(f"Address: {address}")
            print(f"Private key: {temp.priv_key()}")
            return temp.priv_key()


def callback(_):
    pool.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-z", "--zeros", help="Number of zeros to target", type=int, default=5
    )
    args = parser.parse_args()

    start_time = time.time()
    cpus = mp.cpu_count()
    print(f"Mining vanity address with a {args.zeros} zero prefix...")
    print(f"Using {cpus} CPUs...")

    pool = mp.Pool()
    multiple_results = [
        pool.apply_async(gen_addresses, (args.zeros,), callback=callback)
        for _ in range(cpus)
    ]
    pool.close()
    pool.join()
    print(f"Address found in {round(time.time()-start_time, 2)} seconds")
