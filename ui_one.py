import tkinter as tk 

def salvar_pessoa():
    nome = entry_nome.get()
    endereco = entry_endereco.get()
    if nome:
        with open("pessoa.txt","a") as arquivo:
            arquivo.write("Nome: "+ nome +"\nEndereço: " + endereco +"\n")
        label_status.config(text=f'Pessoa "{nome}" salva em endereço "{endereco}" com sucesso!', fg="green")
    else:
        label_status.config(text = "Digite um nome.", fg="red")

root = tk.Tk()
root.title("Pessoa")
root.geometry("350x300")

label_instrucao =tk.Label(root, text = "Digite um nome:")
label_instrucao.pack(pady=10)

entry_nome = tk.Entry(root)
entry_nome.pack(pady=5)

label_instrucao =tk.Label(root, text = "Digite um Endereço:")
label_instrucao.pack(pady=10)

entry_endereco = tk.Entry(root)
entry_endereco.pack(pady=5)

botao_salvar = tk.Button(root, text = "Salvar", command = salvar_pessoa)
botao_salvar.pack(pady=10)

label_status = tk.Label(root, text="")
label_status.pack(pady=5)
root.mainloop()
