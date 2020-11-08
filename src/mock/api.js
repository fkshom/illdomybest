import MockAdapter from 'axios-mock-adapter'
let data = {
  today: "2020-01-01",
  users: [
    { id: 1, name: '田中太郎', dotoday: true },
    { id: 2, name: '鈴木次郎', dotoday: false },
  ]
}
  
export default {
  run: client => {
    const mock = new MockAdapter(client)
    mock.onGet('/members').reply(200, data)
    mock.onPut('/members/1').reply(200, {success: true})
    mock.onPut('/members/2').reply(200, {success: false})
  }
}
