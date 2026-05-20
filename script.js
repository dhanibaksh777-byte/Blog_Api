const API = "http://127.0.0.1:8000"
let token = localStorage.getItem('token')
let username = localStorage.getItem('username')

window.onload = () => {
    localStorage.clear()  
    if (token) {
        showDashboard()
        loadPosts()
    }
}
function showTab(tab) {
    document.getElementById('register').style.display = tab === 'register' ? 'block' : 'none'
    document.getElementById('login').style.display = tab === 'login' ? 'block' : 'none'
    document.getElementById('reg-tab').classList.toggle('active', tab === 'register')
    document.getElementById('log-tab').classList.toggle('active', tab === 'login')
}

function showDashboard() {
    document.getElementById('auth-section').style.display = 'none'
    document.getElementById('dashboard-section').style.display = 'block'
    document.getElementById('nav-username').textContent = `👤 ${username}`
}

async function register() {
    const u = document.getElementById('reg-username').value
    const p = document.getElementById('reg-password').value
    const msg = document.getElementById('reg-msg')

    if (!u || !p) { msg.className = 'error'; msg.textContent = 'Sab fields bharo!'; return }

    try {
        const res = await fetch(`${API}/Register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        })
        const data = await res.json()
        if (data.id) {
            msg.className = 'success'
            msg.textContent = `✅ Account ban gaya! Ab login karo!`
        } else {
            msg.className = 'error'
            msg.textContent = '❌ ' + (data.detail || JSON.stringify(data))
        }
    } catch (e) {
        msg.className = 'error'
        msg.textContent = '❌ Server se connect nahi ho saka!'
    }
}

async function login() {
    const u = document.getElementById('log-username').value
    const p = document.getElementById('log-password').value
    const msg = document.getElementById('log-msg')

    if (!u || !p) { msg.className = 'error'; msg.textContent = 'Sab fields bharo!'; return }

    try {
        const res = await fetch(`${API}/Login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        })
        const data = await res.json()
        if (typeof data === 'string') {
            token = data
            username = u
            localStorage.setItem('token', token)
            localStorage.setItem('username', username)
            showDashboard()
            loadPosts()
        } else {
            msg.className = 'error'
            msg.textContent = '❌ ' + JSON.stringify(data)
        }
    } catch (e) {
        msg.className = 'error'
        msg.textContent = '❌ Server se connect nahi ho saka!'
    }
}

async function createPost() {
    const title = document.getElementById('post-title').value
    const content = document.getElementById('post-content').value
    const msg = document.getElementById('post-msg')

    if (!title || !content) { msg.className = 'error'; msg.textContent = 'Title aur content dono likho!'; return }

    try {
        const res = await fetch(`${API}/posts?token=${token}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
        })
        const data = await res.json()
        if (data.id) {
            msg.className = 'success'
            msg.textContent = '✅ Post publish ho gaya!'
            document.getElementById('post-title').value = ''
            document.getElementById('post-content').value = ''
            loadPosts()
        }
    } catch (e) {
        msg.className = 'error'
        msg.textContent = '❌ Error!'
    }
}

async function loadPosts() {
    try {
        const res = await fetch(`${API}/posts`)
        const posts = await res.json()
        const list = document.getElementById('posts-list')

        if (posts.length === 0) {
            list.innerHTML = '<p style="color:rgba(255,255,255,0.4)">Abhi koi post nahi hai!</p>'
            return
        }

        list.innerHTML = posts.map(post => `
            <div class="post-card">
                <h3>${post.title}</h3>
                <p>${post.content}</p>
                <button class="delete-btn" onclick="deletePost(${post.id})">🗑 Delete</button>
            </div>
        `).join('')
    } catch (e) {
        console.error(e)
    }
}

async function deletePost(id) {
    try {
        const res = await fetch(`${API}/posts/${id}?token=${token}`, {
            method: 'DELETE'
        })
        const data = await res.json()
        if (data.message) loadPosts()
    } catch (e) {
        console.error(e)
    }
}

function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    token = null
    username = null
    document.getElementById('auth-section').style.display = 'flex'
    document.getElementById('dashboard-section').style.display = 'none'
}