const socket = new WebSocket('ws://10.251.176.139:12345');

socket.onopen = function () {
    alert('WebSocket connection established.');
    socket.send("user");
};

// socket.onmessage = function (event) {
//     // alert("recv data from server");
//     // alert(event.data);
//     let data = JSON.parse(event.data);
//     document.getElementById("loc").innerText = data['location'];
//     // document.getElementById("msg").innerText = data['msg']
//     document.getElementById("level").innerText = data['level']

//     let conclusionsItem = document.getElementById("conclusions");
//     conclusionsItem.innerHTML = "";
//     conclusionsItem.innerText = data['text'];
//     // let listItem1 = document.createElement('li');
//     // listItem1.textContent = data['text'];
//     // conclusionsItem.appendChild(listItem1);
//     // for (let i = 0; i < data['text'].length; i++) {
//     //     let listItem = document.createElement('li');
//     //     listItem.textContent = data['text'][i];
//     //     conclusionsItem.appendChild(listItem);
//     // }

//     let adviceItem = document.getElementById("advice");
//     adviceItem.innerHTML = "";
//     let listItem = document.createElement('li');
//     listItem.textContent = data['advice'];
//     adviceItem.appendChild(listItem);

//     // for (let i = 0; i < data['advice'].length; i++) {
//     //     let listItem = document.createElement('li');
//     //     listItem.textContent = data['advice'][i];
//     //     adviceItem.appendChild(listItem);
//     // }
// };

socket.onclose = function () {
    alert('WebSocket connection closed.');
};


// data = {
//     "conclusions": [
//         "hello",
//         "world",
//         "fuck"
//     ]
// }
// let conclusionsItem = document.getElementById("conclusions");
// for (let i = 0; i < data['conclusions'].length; i++) {
//     let listItem = document.createElement('li');
//     listItem.textContent = data['conclusions'][i];
//     conclusionsItem.appendChild(listItem);
// }