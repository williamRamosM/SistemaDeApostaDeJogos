from DAO import usuario_dao

usuario = usuario_dao.Usuario_DAO
nome = "palavra"
if usuario.verificar_name_user(nome) == True:
    print("Bem vindo(a)")
else:
    print("Recusado conection")


    

