import React, { useRef, useState } from 'react'
import './App.css'
import SongList from './song/SongList'

const onlyKana = (str: string): string => {
  const kana = str.replace(/[\u3041-\u3096]/g, function(match) {
      var chr = match.charCodeAt(0) + 0x60;
      return String.fromCharCode(chr);
  });
  return kana.replace(/[^\u30a1-\u30f6]/g, '')
}

function App(): JSX.Element {
  const [chars, setChars] = useState<string>('')
  const [includes, setIncludes] = useState<boolean>(true)

  const charsRef = useRef<HTMLInputElement | null>(null)
  const includesRef = useRef<HTMLSelectElement | null>(null)

  const charsHandler = (event: React.FocusEvent<HTMLInputElement>): void => {
    event.target.value = onlyKana(event.target.value)
  }
  const searchHandler = (): void => {
    setChars(charsRef.current!.value)
    setIncludes(includesRef.current!.value === 'true')
  }
  return (
    <div className="App container is-max-desktop">
      <nav className="navbar is-link" role="navigation" aria-label="main navigation">
        <div className="navbar-brand">
          <p className='navbar-item has-text-weight-bold ml-4'>Radio Kids ドボン(Unofficial)</p>
        </div>
      </nav>
      <div className="box">
        <div className='columns'>
          <div className='column is-vcentered'>
            <p className="label">
              タイトルかアーティスト名に
            </p>
          </div>
          <div className='column'>
            <input
              className="input"
              type="text"
              placeholder="カタカナで入力してください"
              ref={charsRef}
              onBlur={charsHandler}
            ></input>
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
            <button className="button is-link" onClick={searchHandler}>検索</button>
          </div>
        </div>
        <div className='columns'>
          <div className='column is-full'>
            <a href="https://www.k-mix.co.jp/message-kids" target="_blank">リクエストフォーム</a>
          </div>
        </div>
      </div>
      <SongList chars={chars} includes={includes} />
      <footer className="footer">
        <div className="content has-text-centered">
          <p>
            k-mixのラジオ番組 <a href="https://www.k-mix.co.jp/radiokids/" target="_blank">Radio Kids</a>のリクエストテーマは、「曲名・アーティスト名にカorモのいずれかが入っている曲」のような
            ルールがあることがあります。リクエストする曲が思い付かない時に曲を検索してみてください。
          </p>
          <p>
            <strong>Radio Kids ドボン(Unofficial)</strong> by <a href="https://twitter.com/smeghead">@smeghead</a>. 
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
