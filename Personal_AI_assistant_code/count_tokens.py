import tiktoken as tiktoken
import tkinter as tk
from tkinter import filedialog

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # No queremos una ventana completa de Tk, solo el cuadro de diálogo
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if archivo:  # Si se seleccionó un archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
            message = [{"role": "user", "content": texto}]
        num_tokens = num_tokens_from_messages(message)  # Asumimos que num_tokens_from_messages espera una lista
        print(f"El número de tokens en el archivo '{archivo}' es: {num_tokens}")
        print(f"El numero de caracteres en el archivo '{archivo}' es: {len(texto)}, el numero maximo de caracteres aparente es: 32768 para Gpt3.5")
    else:
        print("No se seleccionó ningún archivo.")


if __name__ == "__main__":
    seleccionar_archivo()


