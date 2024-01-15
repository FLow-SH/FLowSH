from datasketch import MinHash, MinHashLSH

def lsh_updater(lsh: MinHashLSH, minhash: MinHash, string: str, token_file: str) -> MinHashLSH:
    '''
        Given the LSH and the MinHash, insert the MinHash inside the LSH and append the
        string and the corresponding key into the token_file

        Parameters:
        lsh (MinHashLSH): the LSH to be used
        minhash (MinHash): the MinHash to the inserted
        string (str): the string to be inserted into the token_file
        token_file (str): the file path of the token_file

        Returns:
        MinHashLSH: the LSH to be used
    '''
    minhash_key = lsh.keys.size() + 1
    exec('lsh.insert("m%s", minhash)' % (str(minhash_key)))
    handle = open(token_file, 'a')
    handle.write('m%s<>%s\n' % (str(minhash_key), string))
    print('lsh updated')
    return lsh