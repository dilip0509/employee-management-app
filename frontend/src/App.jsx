import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [employees, setEmployees] = useState([])
  const [form, setForm] = useState({
    name: '',
    email: '',
    department: ''
  })
  const [editingId, setEditingId] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  const loadEmployees = async () => {
    try {
      const response = await fetch('/employees')
      if (!response.ok) throw new Error('Unable to load employees')
      setEmployees(await response.json())
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadEmployees()
  }, [])

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')

    const url = editingId
      ? `/employees/${editingId}`
      : '/employees'

    try {
      const response = await fetch(url, {
        method: editingId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Operation failed')

      setMessage(editingId ? 'Employee updated successfully!' : 'Employee added successfully!')
      setForm({ name: '', email: '', department: '' })
      setEditingId(null)
      loadEmployees()
    } catch (error) {
      setMessage(error.message)
    }
  }

  const editEmployee = (employee) => {
    setForm({
      name: employee.name,
      email: employee.email,
      department: employee.department
    })
    setEditingId(employee.id)
  }

  const deleteEmployee = async (id) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) return

    try {
      const response = await fetch(`/employees/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Unable to delete employee')

      setMessage('Employee deleted successfully!')
      loadEmployees()
    } catch (error) {
      setMessage(error.message)
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>EMS</h2>
        <p>Employee Management</p>
        <div className="nav-item">▦ Dashboard</div>
        <div className="nav-item active">♙ Employees</div>
      </aside>

      <main className="main">
        <header>
          <div>
            <h1>Employee Management</h1>
            <p>Manage your organization's employees</p>
          </div>
          <span className="admin">Admin</span>
        </header>

        <section className="summary">
          <div className="summary-card">
            <span>Total Employees</span>
            <h2>{employees.length}</h2>
          </div>
          <div className="summary-card">
            <span>Departments</span>
            <h2>{new Set(employees.map(e => e.department)).size}</h2>
          </div>
        </section>

        <section className="content">
          <div className="form-card">
            <h2>{editingId ? 'Edit Employee' : 'Add Employee'}</h2>
            <form onSubmit={handleSubmit}>
              <label>Full Name</label>
              <input name="name" placeholder="Enter employee name"
                value={form.name} onChange={handleChange} required />

              <label>Email Address</label>
              <input name="email" type="email" placeholder="Enter email"
                value={form.email} onChange={handleChange} required />

              <label>Department</label>
              <input name="department" placeholder="Enter department"
                value={form.department} onChange={handleChange} required />

              <button type="submit">
                {editingId ? 'Update Employee' : 'Add Employee'}
              </button>

              {editingId && (
                <button type="button" className="cancel"
                  onClick={() => {
                    setEditingId(null)
                    setForm({ name: '', email: '', department: '' })
                  }}>
                  Cancel
                </button>
              )}
            </form>
            {message && <p className="message">{message}</p>}
          </div>

          <div className="table-card">
            <h2>Employee Directory</h2>
            {loading ? <p>Loading employees...</p> : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Department</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {employees.map(employee => (
                      <tr key={employee.id}>
                        <td>{employee.id}</td>
                        <td>{employee.name}</td>
                        <td>{employee.email}</td>
                        <td>{employee.department}</td>
                        <td>
                          <button className="edit"
                            onClick={() => editEmployee(employee)}>Edit</button>
                          <button className="delete"
                            onClick={() => deleteEmployee(employee.id)}>Delete</button>
                        </td>
                      </tr>
                    ))}
                    {employees.length === 0 && (
                      <tr><td colSpan="5">No employees found.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}
