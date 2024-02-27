<script>
  // @ts-nocheck

  import { onMount } from "svelte";

  let todo = "";
  let todoList = [];
  let bool = false;
  let isEditEnabled = false;
  let editId = "";
  let completeID;

  onMount(() => {
    const token = localStorage.getItem("token") || null;

    if (!token) {
      window.location.href = "/";
    }
  });

  onMount(async () => {
    try {
      const response = await fetch("http://localhost:5000/todos");

      const data = await response.json();

      todoList = data.todos;
    } catch (error) {
      console.log("Error while getting todos", error);
    }
  });
// adding the todo
  const addTodo = async () => {
    if (!todo.trim()) {
      todo = "";
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/todos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ todo }),
// object to string converting
      });

      const data = await response.json();

      todoList = [...todoList, data.todo];

      console.log("todoList", todoList);

      todo = "";
    } catch (error) {
      console.log("error is adding todo", error);
    }
  };

  // removing the element
  const removeTodo = async (todoId) => {
    const response = await fetch(`http://localhost:5000/remove/${todoId}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (data.success === true) {
      todoList = todoList.filter((todo) => todo["_id"]["$oid"] !== todoId);
      console.log("todoList", todoList);
    }
  };

  // editing the todo item
  const updateTodo = async () => {
    const response = await fetch(`http://localhost:5000/update/${editId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ new_task: todo }),
    });
    const data = await response.json();
    console.log("data", data);

    if (data.success) {
      todoList = todoList.map((item) => {
        if (item["_id"]["$oid"] === editId) {
          item.todo_item = todo;
        }
        return item;
      });

      todo = "";
      isEditEnabled = false;
    }
  };
  // updating the task
  const editTask = async (todo_Id) => {
    const index = todoList.findIndex((todo) => todo._id["$oid"] === todo_Id);
    todo = todoList[index].todo_item;
    isEditEnabled = true;
    editId = todo_Id;
  };

  // task completing
  const handleCompleted = async (todoId, e) => {
    // console.log("isCompleted:", e);
    const response = await fetch(`http://localhost:5000/complete/${todoId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ isCompleted: e.target.checked }),
    });
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };
</script>

<body>
  <div class="logout">
    <button on:click={handleLogout}>LogOut</button>
  </div>
  <h1 id="header">To-Do List Application</h1>

  <div id="form-container">
    <input bind:value={todo} placeholder="Add your Task here...." />

    {#if isEditEnabled}
      <button id="update-btn" type="submit" on:click={updateTodo}>Update</button
      >
    {/if}
    {#if !isEditEnabled}
      <!-- svelte-ignore missing-declaration -->
      <button id="add-btn" type="submit" on:click={addTodo}>Add Task</button>
    {/if}
  </div>

  {#each todoList as todo}
    <div class="task-container">
      <div>
        <input
          bind:checked={todo.isCompleted}
          on:click={(e) => handleCompleted(todo["_id"]["$oid"], e)}
          type="checkbox"
        />
        <span style={todo.isCompleted ? "text-decoration: line-through" : ""}
          >{todo.todo_item}
        </span>
      </div>
      <div>
        <button on:click={() => editTask(todo["_id"]["$oid"])}>Edit</button>
        <button id="delete-btn" on:click={() => removeTodo(todo["_id"]["$oid"])}>Delete</button>
      </div>
    </div>
  {/each}
</body>

<style>
  body {
    text-align: center;
    font-family: Arial, sans-serif;
    /* background-color: rgba(241, 162, 162, 0.5); */
    background-color: rgb(137, 175, 183);
  }

  .logout {
    text-align: right;
    padding: 10px;
  }

  .logout button {
    padding: 10px 15px;
    background-color:palevioletred;
  }

  button {
    background: rgb(208, 159, 198);
    border: 10px;
    color: white;
    padding: 5px;
    border-radius: 5px;
    cursor: pointer;
    transition: 0.4s ease;
  }

  #form-container {
    width: 50%;
    margin: auto;
  }

  #form-container input {
    padding: 6px 8px;
    border-radius: 5px;
    border: none;
  }

  #form-container button {
    padding: 8px 10px;
  }

  .task-container {
    display: flex;
    width: 22%;
    margin: auto;
    margin-top: 10px;
    padding: 0 20px;
    justify-content: space-between;
  }

  #delete-btn {
    background-color: rgb(232, 58, 58);
  }
</style>
