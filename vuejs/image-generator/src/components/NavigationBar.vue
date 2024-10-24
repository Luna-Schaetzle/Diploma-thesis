<template>
  <nav>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/gallery">Galerie</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
nav {
    background-color: #333;
    padding: 10px;
}

ul {
    list-style-type: none;
    display: flex;
    gap: 15px;
}

li {
    color: white;
}
</style>
