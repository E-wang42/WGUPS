class HashTable:
    def __init__(self, capacity=40):
        # Initialize the hash table with a given capacity, defaulting to 40.
        # The table is represented as a list of empty lists (buckets) to handle collisions.
        self.capacity = capacity
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, item):
        # Insert a key-item pair into the hash table.
        # The hash value of the key determines the bucket where the item will be stored.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # If the key already exists in the bucket, update its value.
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If the key does not exist, append the new key-item pair to the bucket.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def get(self, key):
        # Retrieve an item from the hash table using its key.
        # The hash value of the key determines the bucket to search in.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key in the bucket and return the associated item if found.
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None  # Return None if the key is not found.

    def remove(self, key):
        # Remove a key-item pair from the hash table.
        # The hash value of the key determines the bucket to search in.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key in the bucket and remove the key-item pair if found.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
