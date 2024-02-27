<script>
  // @ts-nocheck

  import axios from "axios";

  let username, password, email;
  const handleSignup = async () => {
    try {
      console.log(username, email, password);
      const response = await axios.post("http://localhost:5000/signup", {
        username: username,
        email: email,
        password: password,
      });

      if (response.data.success) {
        alert("Sign up successful");
        window.location.href = "/";
      } else {
        alert("Sign up failed. Please check your details and try again.");
      }
    } catch (error) {
      console.error("Error during signup:", error);
      alert("An error occurred during signup. Please try again later.");
    }
  };
</script>

<body>
  <div>
    <h2>Sign Up</h2>

    <form on:submit|preventDefault={handleSignup}>
      <label for="username">Username</label>
      <input type="text" name="username" bind:value={username} required /><br />
      <label for="email">Email</label>
      <input type="email" name="email" bind:value={email} required /><br />
      <label for="password">Password</label>
      <input
        type="password"
        name="password"
        bind:value={password}
        required
      /><br />
      <button>Register</button>
    </form>

    <p>Already have an account? <a href="/">Login</a>.</p>
  </div>
</body>

<style>
  body {
    font-family:'Times New Roman', Times, serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80vh;
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
    margin-bottom: 5px;
    color:white;
    
  }

  input {
    padding: 10px;
    margin-bottom: 5px;
    border: 1px solid #e8e6e6;
    border-radius: 5px;

    
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