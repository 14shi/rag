def validate_user(email, password):
    # 这里使用硬编码的用户数据进行验证，生产项目中需要用数据库维护邮箱和密码
    valid_users = {
        'admin@qq.com': '123456'
    }
    if email in valid_users and password == valid_users[email]:
        return True
    return False