<script>
  // @ts-nocheck

  import axios from "axios";
  let email, password;

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:5000/login", {
        email: email,
        password: password,
      });

      console.log("response", response);

      if (response.data.success === true) {
        localStorage.setItem("token", response.data.token);
        console.log("response.data.token", response.data.token);
        window.location.href = "/about";
      } else {
        alert("User Not found please signup.");
        window.location.href = "/signup";
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };
</script>

<body>
  <div class="login">
    <h2>Login Page</h2>
    <form class="form" on:submit|preventDefault={handleLogin}>
      <label for="email">Email address:</label>
      <input type="email" bind:value={email} required /><br />
      <label for="password">Password:</label>
      <input
        type="password"
        name="password"
        bind:value={password}
        required
      /><br />
      <button>Login</button>
    </form>
    <br />
    <br />
    <p>Don't have an account? <a href="/signup">Register here</a></p>
  </div>
</body>

<style>
  body {
    font-family:'Times New Roman', Times, serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: rgb(137, 175, 183);
  
  }

 
  h2 {
    text-align: center;
    color:white;
  }

  form {
    display: flex;
    flex-direction: column;
  }

  label {
    margin-bottom: 10px;
    color:white;
    
  }

  input {
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #e8e6e6;
    border-radius: 10px;

    
  }
  input:hover{
    background-color:rgb(224, 213, 223);
  }

  button {
    background-color: #bc0c9c;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: medium;
    font-weight: bold;
  }

  button:hover {
    background-color:rgb(219, 61, 180);
  }
  p{
    color: white;
  }
</style> 
