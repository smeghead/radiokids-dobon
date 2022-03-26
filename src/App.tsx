import React, { useRef, useState } from 'react'
import './App.css'
import SongList from './song/SongList'

function App(): JSX.Element {
  const [chars, setChars] = useState<string>('')
  const [includes, setIncludes] = useState<boolean>(true)

  const charsRef = useRef<HTMLInputElement | null>(null)
  const includesRef = useRef<HTMLSelectElement | null>(null)

  const searchHandler = (): void => {
    setChars(charsRef.current!.value)
    setIncludes(includesRef.current!.value === 'true')
  }
  return (
    <div className="App container is-max-desktop">
      <nav className="navbar" role="navigation" aria-label="main navigation">
        <div className="navbar-brand">
          <p className='navbar-item'>Radio Kids ドボン(Unofficial)</p>
        </div>
      </nav>
      <div className='box columns'>
        <div className='column is-half'>
          <input className="input" type="text" placeholder="条件となる文字を入力してください" ref={charsRef}></input>
        </div>
        <div className='column'>
          <div className='select is-normal'>
            <select ref={includesRef}>
              <option value={'true'}>を含む</option>
              <option value={'false'}>を含まない</option>
            </select>
          </div>
        </div>
        <div className='column'>
          <button className="button is-primary" onClick={searchHandler}>検索</button>
        </div>
      </div>
      <SongList chars={chars} includes={includes} />
    </div>
  )
}

export default App
