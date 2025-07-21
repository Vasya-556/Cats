'use client'

import { useEffect, useState } from 'react'

type SpyCat = {
  id: number
  name: string
  years_of_experience: number
  breed: string
  salary: string
}

export default function Page() {
  const [cats, setCats] = useState<SpyCat[]>([])
  const [form, setForm] = useState({ name: '', years_of_experience: '', breed: '', salary: '' })
  const [editingId, setEditingId] = useState<number | null>(null)
  const [editSalary, setEditSalary] = useState('')
  const [error, setError] = useState('')

  const loadCats = async () => {
    const res = await fetch('http://localhost:8000/cats/spycats/')
    const data = await res.json()
    console.log(data);
    setCats(data)
  }

  useEffect(() => {
    loadCats()
  }, [])

  const addCat = async () => {
    setError('')
    const res = await fetch('http://localhost:8000/cats/spycats/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.name,
        years_of_experience: parseInt(form.years_of_experience),
        breed: form.breed,
        salary: form.salary
      })
    })
    if (!res.ok) {
      const data = await res.json()
      setError(data.breed || 'Failed to add cat')
      return
    }
    setForm({ name: '', years_of_experience: '', breed: '', salary: '' })
    loadCats()
  }

  const deleteCat = async (id: number) => {
    await fetch(`http://localhost:8000/cats/spycats/${id}/`, { method: 'DELETE' })
    loadCats()
  }

  const startEdit = (id: number, salary: string) => {
    setEditingId(id)
    setEditSalary(salary)
  }

  const saveSalary = async () => {
    if (!editingId) return
    await fetch(`http://localhost:8000/cats/spycats/${editingId}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ salary: editSalary })
    })
    setEditingId(null)
    setEditSalary('')
    loadCats()
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Spy Cats Dashboard</h1>

      <div className="mb-6 space-y-2">
        <input className="border w-full p-2" placeholder="Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <input className="border w-full p-2" placeholder="Years of Experience" value={form.years_of_experience} onChange={e => setForm({ ...form, years_of_experience: e.target.value })} />
        <input className="border w-full p-2" placeholder="Breed" value={form.breed} onChange={e => setForm({ ...form, breed: e.target.value })} />
        <input className="border w-full p-2" placeholder="Salary" value={form.salary} onChange={e => setForm({ ...form, salary: e.target.value })} />
        <button className="bg-blue-600 text-white px-4 py-2" onClick={addCat}>Add Cat</button>
        {error && <div className="text-red-500">{error}</div>}
      </div>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100 text-blue-600">
            <th className="p-2 border">Name</th>
            <th className="p-2 border">Experience</th>
            <th className="p-2 border">Breed</th>
            <th className="p-2 border">Salary</th>
            <th className="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          {cats.map(cat => (
            <tr key={cat.id} className="text-center border-t">
              <td className="p-2 border">{cat.name}</td>
              <td className="p-2 border">{cat.years_of_experience}</td>
              <td className="p-2 border">{cat.breed}</td>
              <td className="p-2 border">
                {editingId === cat.id ? (
                  <input value={editSalary} onChange={e => setEditSalary(e.target.value)} className="border p-1 w-24" />
                ) : cat.salary}
              </td>
              <td className="p-2 border space-x-2">
                {editingId === cat.id ? (
                  <button className="bg-green-600 text-white px-2 py-1" onClick={saveSalary}>Save</button>
                ) : (
                  <button className="bg-yellow-500 text-white px-2 py-1" onClick={() => startEdit(cat.id, cat.salary)}>Edit</button>
                )}
                <button className="bg-red-600 text-white px-2 py-1" onClick={() => deleteCat(cat.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}