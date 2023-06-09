def client_key_params_func():
    import firebase_admin
    from firebase_admin import firestore, credentials
    import json

    cred = credentials.Certificate(r'thresholdcryptochat-firebase-adminsdk-efq0t-9f4616190a (2).json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    user_name = u'kateryna'

    # Read crypto parameters from firestore db
    read_ref = db.collection(u'key_params')
    read_ref = read_ref.where(u'user', u'==', user_name)
    for doc in read_ref.stream():
        key_parameters = doc.to_dict()

    # Save crypto parameters to 'key_parameters.json' file
    with open('key_parameters.json', 'w') as json_file:
        json.dump(key_parameters, json_file)