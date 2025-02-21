import { useState } from "react";

const SignIn = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault()

        const opts = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        }

        const res = await fetch("http://localhost/api/users", opts)
        const data = await res.json()

        if (!res.ok) {
            setErrorMsg(data.detail)
            return
        }
    }

    return (
        <form onSubmit={onSubmit}>  
            <h2>SignIn</h2>
            <label>Username</label>
            <input type="text" name="username" onChange={e => setUsername(e.target.value)} value={username}/>

            <br />

            <label>Email</label>
            <input type="email" id="email" name="email" onChange={e => setEmail(e.target.value)} value={email}/>

            <br />

            <label>Password</label>
            <input type="password" id="password" name="password" onChange={e => setPassword(e.target.value)} value={password}/>

            <br />


            {errorMsg ? <p>{errorMsg}</p> : ""}

            <button type="submit" value="login">SignIn</button>
        </form>
    )
}

export default SignIn