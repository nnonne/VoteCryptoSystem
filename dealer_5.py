def dealer_5_func():
    import firebase_admin
    from firebase_admin import firestore, credentials
    from threshold_crypto_library import ThresholdCrypto, ThresholdParameters
    import uuid


    cred = credentials.Certificate(r'thresholdcryptochat-firebase-adminsdk-efq0t-9f4616190a (2).json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    users = [u'karina', u'dmytro', u'pavlo', 'kateryna', 'yaroslav']

    def clear_collection(db, collection):
        data = db.collection(collection)
        for d in data.stream():
            d.reference.delete()

    clear_collection(db, u'key_params')


    def create_crypto_params_int(n=5, t=3):

        key_params = ThresholdCrypto.static_2048_key_parameters()
        thresh_params = ThresholdParameters(t, n)
        pub_key, key_shares = ThresholdCrypto.create_public_key_and_shares_centralized(key_params, thresh_params)
        p = key_params.p
        q = key_params.q
        g = key_params.g
        pub_key = pub_key.g_a
        share1 = [key_shares[0].x, key_shares[0].y]
        share2 = [key_shares[1].x, key_shares[1].y]
        share3 = [key_shares[2].x, key_shares[2].y]
        share4 = [key_shares[3].x, key_shares[3].y]
        share5 = [key_shares[4].x, key_shares[4].y]

        return p, q, g, n, t, pub_key, share1, share2, share3, share4, share5


    def create_crypto_params_str(p, q, g, n, t, pub_key, share1, share2, share3, share4, share5):

        p = str(p)
        q = str(q)
        g = str(g)
        pub_key = str(pub_key)
        share1 = [share1[0], str(share1[1])]
        share2 = [share2[0], str(share2[1])]
        share3 = [share3[0], str(share3[1])]
        share4 = [share4[0], str(share4[1])]
        share5 = [share5[0], str(share5[1])]

        return p, q, g, n, t, pub_key, share1, share2, share3, share4, share5


    p, q, g, n, t, pub_key, share1, share2, share3, share4, share5 = create_crypto_params_int()
    p, q, g, n, t, pub_key, share1, share2, share3, share4, share5 = create_crypto_params_str(
                                                                     p, q, g, n, t, pub_key,share1, share2, share3, share4, share5)
    shares = [share1, share2, share3, share4, share5]

    i = 0
    for user in users:
        doc_ref = db.collection(u'key_params').document(str(uuid.uuid4()))
        doc_ref.set({u'user': user, u'p': p, u'q': q, u'g': g, u'n': n, u't': t, u'pub_key': pub_key, u'share': shares[i]})
        i += 1