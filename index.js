const express = require('express')
const {exec} = require('child_process');
const readline = require('readline');
const fs = require('fs');
var url = require('url');
const app = express()
const port = 3000
app.get('/', (req, res) => {
  var d = new Date();
  var n = d.getTime();

  namafile = {namafile:n+".txt"};
  // json = JSON.parse(namafile)
  // res.send()
  var q = url.parse(req.url, true);
  console.log(q.query);
  // console.log(q.query.id);
  // var cmd = 'python ssh.py surv2-apps 10.62.170.49 '++' 23 garudaadh038 "show port" >>'+n+'.txt';
  if (typeof q.query.ip !== 'undefined') {
    // res.send("bro");

    res.send(namafile);
    var command = 'python ssh.py surv2-apps 10.62.170.49 '+q.query.ip+' 23 garudaadh038 "show card state">>'+n+'.txt';
    // var command = "python ssh.py 930053 10.62.165.4 172.28.115.42 23 Mojave2020 >>"+n+".txt";
    // res.send(command);
    // "python ssh.py 930053 10.62.165.4 172.28.115.42 23 Mojave2020 >>"+n+".txt"
    console.log(command);
    exec(command, (error, stdout, stderr) => {

      console.log(`stdout: ${stdout}`);

      // res.send( ) );

    });
  }
  if (typeof q.query.routerport !== 'undefined' && typeof q.query.port !== 'undefined') {
    // res.send("bro");

    res.send(namafile);
    var command = 'python ssh.py surv2-apps 10.62.170.49 '+q.query.routerport+' 23 garudaadh038 "show card state">>'+n+'.txt';
    // var command = "python ssh.py 930053 10.62.165.4 172.28.115.42 23 Mojave2020 >>"+n+".txt";
    // res.send(command);
    // "python ssh.py 930053 10.62.165.4 172.28.115.42 23 Mojave2020 >>"+n+".txt"
    console.log(command);
    exec(command, (error, stdout, stderr) => {

      console.log(`stdout: ${stdout}`);

      // res.send( ) );

    });
  }

})
app.listen(port, () => console.log(`Example app listening on port ${port}!`))
