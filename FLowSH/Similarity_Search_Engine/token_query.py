from datasketch import MinHash, MinHashLSH

def token_query(lsh: MinHashLSH, minhash: MinHash) -> list[str]:
    '''
        Given the LSH and the minHash, returns the number of keys
        the MinHash is similar to

        Parameters:
        lsh(MinHashLSH): the LSH to be used
        minhash(MinHash): the Minhash to be used

        Returns:
        list[str]: the list of strings
    '''
    return lsh.query(minhash)
