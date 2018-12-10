import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';

void main() => runApp(new MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Real time Twitter dashbord',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PhotoList(),
    );
  }
}

class PhotoList extends StatefulWidget {
  @override
  PhotoListState createState() => PhotoListState();
}

class PhotoListState extends State<PhotoList> {
  List<Twitt> list = [];
  IOWebSocketChannel channel;

  @override
  void initState() {
    super.initState();
    channel = new IOWebSocketChannel.connect("ws://176.38.3.7:8888/ws/");

    channel.stream.listen((message) => setState(() => list.add(Twitt.fromJsonMap(message))));
  }

  @override
  void dispose() {
    super.dispose();
    channel.sink.close();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Real time Twitter dashbord"),
      ),
      body: Center(
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemBuilder: (BuildContext context, int index) => _makeElement(index),
        ),
      ),
    );
  }

  Widget _makeElement(int index) {
    if (index >= list.length) {
      return null;
    }

    return Container(
        padding: EdgeInsets.all(5.0),
        child: Padding(
          padding: EdgeInsets.only(top: 200.0),
          child: Column(
            children: <Widget>[
              Image.network(list[index].url, width: 150.0, height: 150.0),
              Text(list[index].text),
            ],
          ),
        ));
  }
}

class Twitt {
  final String text;
  final String url;

  Twitt.fromJsonMap(Map map)
      : text = map['title'],
        url = map['url'];
}
