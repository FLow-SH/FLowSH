from datasketch import MinHash, MinHashLSH

def token_builder(string:str, shingle_size:int, num_permutation:int) -> MinHash:
    '''
        Give the string, the shingle size and the number of permutations, creates the
        MinHash of that string.

        Parameters:
        string(str): the string to be minHashed
        shingle_size(int): the size of a shingle
        num_permutations(int): the number of permutations

        Returns:
        MinHash: the MinHash of the string
    '''
    if len(string) < shingle_size + 1:  
        n = MinHash(num_perm=num_permutation)
        n.update(string.encode('utf8'))
        return n

    list_of_shingles:set[str] = set() 

    for n in range(0, len(string)-shingle_size-1, 1):
        new_s = (string[n:n+shingle_size])
        list_of_shingles.add(new_s)

    n = MinHash(num_perm=num_permutation)

    for d in list_of_shingles:
        n.update(d.encode('utf8'))
    return n