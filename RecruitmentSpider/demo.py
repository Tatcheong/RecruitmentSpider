from redis import StrictRedis, ConnectionPool

# url = 'redis://foobared@spider1:6379/0'
#
# pool = ConnectionPool.from_url(url)
# redis = StrictRedis(connection_pool=pool)
redis = StrictRedis(host='spider1', port=6379, db=0, password='foobared')
redis.set('age', '22')
print(redis.get('age'))