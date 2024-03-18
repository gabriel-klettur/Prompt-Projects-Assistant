from openai import OpenAI
import time

BABALU_ASSISTANT_ID = "asst_OrLBfAr78vxpeeIFrsrGhFkK"  # or a hard-coded ID like "asst-..."

client = OpenAI()

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# La primera vez que se consulta el asistente, se crea el hilo de conversacion.
# Si se vuelve a ejecutar esta funcion, se crearan nuevos hilos de conversacion.
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(BABALU_ASSISTANT_ID, thread, user_input)
    return thread, run

#
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

# Pretty printing helper
def pretty_print(messages):
    print("# Messages ---------------------------------------------------------------------")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Emulating concurrent user requests
thread1, run1 = create_thread_and_run("Necesito una receta de masa de pizza")
thread2, run2 = create_thread_and_run("Puedes darme una receta de galletas con melocoton?")
thread3, run3 = create_thread_and_run("podrias explicarme como limpiar una cocina?")
# Now all Runs are executing...

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# Wait for Run 1
run1 = wait_on_run(run1, thread1)
pretty_print(get_response(thread1))

# Wait for Run 2
run2 = wait_on_run(run2, thread2)
pretty_print(get_response(thread2))

# Wait for Run 3
run3 = wait_on_run(run3, thread3)
pretty_print(get_response(thread3))

# Thank our assistant on Thread 3 :)
run4 = submit_message(BABALU_ASSISTANT_ID, thread3, "Thank you!")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))

run4 = submit_message(BABALU_ASSISTANT_ID, thread3, "Podrias darme otro concejo de Cocina?")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))

run4 = submit_message(BABALU_ASSISTANT_ID, thread3, "Como puedo llegar a ser el mejor cocinero del mundo?")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))



