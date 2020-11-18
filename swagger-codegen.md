# Generating a client with Swagger Code Generation tool

VoiceBase V3 API follows the OpenAPI 2.0 Specification  (also known as Swagger RESTful API Documentation Specification).

By following the specification, the API is documented in a way that code generation tools can understand, saving you time and effort on generating code to build requests or access the response from the API.

The VoiceBase V3 OpenAPI specification resides at https://apis.voicebase.com/v3/defs/v3-api.yaml

This document is a summary of how to use the Swagger Code Generation tool to generate a VoiceBase V3 client.
We assume that you already have installed Java 8 and Maven.

## Download Swagger Codegen CLI tool

The following command uses Maven to download the Swagger Codegen tool.
```sh
mvn dependency:copy -Dartifact=io.swagger:swagger-codegen-cli:2.2.2 -DoutputDirectory=. -Dmdep.stripVersion=true
```


## Generating a client
Swagger Codegen allows you to generate a client in a wide variety of languages. You may check if your preferred programming language is available by executing
```sh
java -jar swagger-codegen-cli.jar langs
```
Here is a sample of the results:
```
Available languages: [android, aspnet5, aspnetcore, async-scala, bash, cwiki, csharp,
cpprest, dart, elixir, flash, python-flask, go, groovy, java, jaxrs, jaxrs-cxf-client,
jaxrs-cxf, jaxrs-resteasy, jaxrs-resteasy-eap, jaxrs-spec, jaxrs-cxf-cdi, inflector,
javascript, javascript-closure-angular, jmeter, nancyfx, nodejs-server, objc, perl,
php, python, qt5cpp, ruby, scala, scalatra, finch, silex-PHP, sinatra, rails5, slim,
spring, dynamic-html, html, html2, swagger, swagger-yaml, swift, swift3, tizen,
typescript-angular2, typescript-angular, typescript-node, typescript-fetch, akka-scala,
CsharpDotNet2, clojure, haskell, lumen, go-server, erlang-server, undertow, msf4j, ze-ph]
```
The client code generation for a given programming language can be customized with several options. You can get a list of available options by executing
```sh
java -jar swagger-codegen-cli.jar config-help -l <language>
```
For example, if you want to know what options are available for the Scala language:
```sh
java -jar swagger-codegen-cli.jar config-help -l scala
```
### Generating client code for Java
```sh
java -jar swagger-codegen-cli.jar generate  \
     -i https://apis.voicebase.com/v3/defs/v3-api.yaml \
     -l java \
     -c java-config.json \
     -o v3client
```
Where `java-config.json` is the file with the options for the generator:

```json
{
  "modelPackage" : "com.example.v3client.model",
  "apiPackage"   : "com.example.v3client.api",
  "invokerPackage" : "com.example.v3client",
  "groupId" : "com.example.v3",
  "artifactId"  : "v3client",
  "fullJavaUtil" : true,
  "dateLibrary" : "java8",
  "library" :  "jersey2"
}   
```

With the generated client, you may now submit a media for processing

```java
  String baseApiUrl = "https://apis.voicebase.com/";
  String v3Token = "your-token-goes here";
  int connectTimeout = 60000;
  int readTimeout = 120000;

  // Create an ApiClient per thread
  ApiClient client = new ApiClient();

  client.setBasePath(baseApiUrl);
  client.setApiKey("Bearer " + v3Token);
  client.setConnectTimeout(connectTimeout);
  client.setDebugging(true);

  MediaApi mediaApi = new MediaApi(client);

  ObjectMapper objectMapper = new ObjectMapper();
  objectMapper.configure(SerializationFeature.WRITE_EMPTY_JSON_ARRAYS, false);
  objectMapper.configure(SerializationFeature.WRITE_NULL_MAP_VALUES, false);
  objectMapper.configure(SerializationFeature.INDENT_OUTPUT, true);
  objectMapper.setSerializationInclusion(Include.NON_NULL);

  File mediaFile = new File("stereo-recording.wav");

  // Create the configuration programmatically
  VbConfiguration configuration = new VbConfiguration();
  VbStereoConfiguration stereo = new VbStereoConfiguration();
  VbChannelConfiguration leftChannel = new VbChannelConfiguration();
  leftChannel.setSpeakerName("Agent");
  stereo.setLeft(leftChannel);
  VbChannelConfiguration rightChannel = new VbChannelConfiguration();
  rightChannel.setSpeakerName("Caller");
  stereo.setRight(rightChannel);
  VbIngestConfiguration ingest = new VbIngestConfiguration();
  ingest.setStereo(stereo);
  configuration.setIngest(ingest);
  String strConfiguration = objectMapper.writeValueAsString(configuration);

  // And execute the request
  VbMedia upload = mediaApi.postMedia(mediaFile, null, strConfiguration, null, null);
  String mediaId = upload.getMediaId();

```

Alternatively, you could build the configuration yourself as a JSON string
```java
   strConfiguration = "{'ingest': { 'stereo': { 'left': { 'speakerName' : 'Agent' }, 'right':{ 'speakerName' : 'Caller' }}}}";
   VbMedia upload = mediaApi.postMedia(mediaFile, null, strConfiguration , null, null );
```


 Later on, you could retrieve the analytics and transcripts:

```java      
  VbMedia analytics = mediaApi.getMediaById(mediaId, null);
  switch (analytics.getStatus()) {
      case FINISHED:
          // Keywords
          if( analytics.getKnowledge() != null && analytics.getKnowledge().getKeywords() != null) {
              System.out.println("**** Keywords: ");
              for( VbKeyword keyword : analytics.getKnowledge().getKeywords() ) {
                  System.out.println( keyword.getKeyword() );
              }
          }
          // Topics
          if( analytics.getKnowledge() != null && analytics.getKnowledge().getTopics() != null) {
              System.out.println("**** Topics: ");
              for(  VbTopic topic : analytics.getKnowledge().getTopics()) {
                  System.out.println( topic.getTopicName() );
              }
          }

          // Retrieving the text transcript
          String text = mediaApi.getTextById(mediaId);
          System.out.println(text);

          break;
      case FAILED:
          System.out.println("Transcription failed");
          break;
      default:
          System.out.println("Results not yet available, please wait...");
          break;
  }  
```
