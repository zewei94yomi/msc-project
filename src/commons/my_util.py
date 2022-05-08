import shortuuid


def get_uuid():
    return shortuuid.ShortUUID(alphabet="0123456789").random(8)


if __name__ == '__main__':
    print("Main test...")