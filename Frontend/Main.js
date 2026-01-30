// ==========================
// LOGIN
// ==========================
document.addEventListener("DOMContentLoaded", () => {

  const loginBtn = document.getElementById("submitbtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", loginUser);
  }

  const signupBtn = document.getElementById("submitbtn");
  if (signupBtn && document.getElementById("confirmpassword")) {
    signupBtn.addEventListener("click", signupUser);
  }

});

async function loginUser() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.status === 200) {
      alert("Login successful 🚀");
      // window.location.href = "dashboard.html";
    } else {
      alert(data.message || "Invalid credentials");
    }

  } catch (error) {
    console.error(error);
    alert("Server error");
  }
}


// ==========================
// SIGNUP
// ==========================
async function signupUser() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmpassword").value.trim();
  const location = document.getElementById("location").value.trim();

  if (!email || !password || !confirmPassword || !location) {
    alert("Please fill all fields");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match ❌");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        location
      })
    });

    const data = await response.json();

    if (response.status === 200 || response.status === 201) {
      alert("Signup successful 🚀");
      window.location.href = "Login.html";
    } else {
      alert(data.message || "Signup failed");
    }

  } catch (error) {
    console.error(error);
    alert("Server error");
  }
}


