<template>
  <div id="app">
    <div class="jumbotron">I'll do my best today!<br>{{this.today}}</div>
    <div class="container">
      <!-- https://bootstrap-vue.org/docs/components/alert -->
      <b-alert v-model="showflash" v-bind:variant="flashmessagestyle" dismissible fade>
        {{ this.flashmessage }}
      </b-alert>
      <ul class="list-unstyled">
      <li v-for="member in members" :key="member.id">
        <div class="row">
          <div class="col-xs-2">
            {{ member.name }}
          </div>
          <div class="col-xs-2">
          <b-form-checkbox
          :id="'checkbox-' + member.id"
          v-model="member.dotoday"
          name="'checkbox-' + member.id"
          switch
          v-on:change="changeCheckbox(member.id, $event)"
          >
          </b-form-checkbox>
          </div>
          <div class="col-xs-1">
            <a v-on:click="showEditForm">[Edit]</a>
          </div>
        </div>
      </li>
      </ul>
      <pre>
今日は残業をします。
メンバー名：{{ members.filter(m => m.dotoday == true).map(m => m.name).join(",") }}
      </pre>
      <vue-c3 :handler="handler"></vue-c3>
    </div>
  </div>
</template>

<script>
import Api from './apis/api.js'
import Vue from 'vue'
import VueC3 from 'vue-c3'
import 'c3/c3.min.css'
export default {
  name: 'App',
  components: {
    VueC3
  },
  data() {
    return {
      today: "",
      showflash: false,
      flashmessage: "mess",
      flashmessagestyle: "primary",
      members: [],
      status: false,
      handler: new Vue(),
    }
  },
  mounted() {
    this.getMembers()
    //history = this.getHistory()
    let historydata = [
      {name: "田中", data: [1,2,3,1,2,1]},
      {name: "鈴木", data: [1,2,3,1,2,1]},
    ]
    let columns = []
    let groups = []
    historydata.forEach(hist => {
      columns.push([hist.name, ...hist.data])
      groups.push(hist.name)
      
    });
    const options = {
      data: {
        columns: columns,
        type: 'bar',
        groups: [
          groups
        ]
      },
      // axis: {
      //   x: {
      //     type: 'category',
      //     categories: ['at1', 'cat2']
      //   }
      // }
    }
    this.handler.$emit('init', options)
  },
  methods: {
    getHistory() {
      Api.getHistory()
        .then(response => {
          return response.data
        })
        .catch(error => {
          console.error(error)
          this.showFlashMessage("履歴情報の取得に失敗しました。", "danger")
        })
    },
    showFlashMessage(message, style) {
      this.flashmessage = message
      this.flashmessagestyle = style
      this.showflash = true
    },
    changeCheckbox (id, event) {
      //event = true or false
      console.log(this.members)
      console.log(id)
      console.log(event)
      const name = this.members.find(member => member.id === id).name
      Api.setDoToday(id, event)
        .then(response => {
          console.log(response)
          if(response.data.success) {
            if(event == true){
              this.showFlashMessage(`${name}さん 無理をせずにがんばってください`, "success")
            } else {
              this.showFlashMessage(`${name}さん あばたはビジネスマンの鏡です。`, "success")
            }
          } else {
            this.showFlashMessage("サーバーでの処理に失敗しました。", "danger")
            const member = this.members.find(member => member.id === id)
            if(member) {
              member.dotoday = !event
            }
          }
        })
        .catch(error => {
          console.error(error)
          this.showFlashMessage("サーバーでの処理に失敗しました。", "danger")
          const member = this.members.find(member => member.id === id)
          if(member) {
            member.dotoday = !event
          }
        })
    },
    getMembers () {
      Api.getMembers()
        .then(response => {
          console.log(response.data)
          this.today = response.data.today
          this.members = response.data.users
        })
        .catch(error => {
          this.showFlashMessage("情報の取得に失敗しました。", "danger")
          console.error(error)
        })
    },
    showEditForm() {
      this.showFlashMessage("Not Implemented", "danger")
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.fade-enter-active {
  transition: opacity 1s ease;
}
.fade-leave-active {
  transition: opacity 3s ease;
}
.fade-enter, .fade-leave-to{
  opacity: 0;
}
</style>
