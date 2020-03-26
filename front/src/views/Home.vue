<!--suppress SpellCheckingInspection -->
<template>
  <div class="home">
    <div :key ="index" v-for="(conversation, index) in conversations">
      {{ conversation.title }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Home",
  components: {},
  data() {
    return {
      conversations: null,
    }
  },
  mounted() {
    axios.get('http://127.0.0.1:7000/conversation')
      .then((response) => {
        const data = response['data'];

        if (data) {
          this.conversations = data;
        }
      })
      .catch((e) => console.log(e));
    },
}
</script>

<style scoped>

</style>