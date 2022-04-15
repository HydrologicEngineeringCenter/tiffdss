#include "json/json.h"
#include <iostream>
#include <fstream>
using std::string;
using std::cout;

int main() {
  Json::Value root;  
  string fn = "../../dss-test-data/tiff/packager-example.json";
  std::ifstream config_doc(fn, std::ifstream::binary);
  config_doc >> root;
  //std::cout << root;
  Json::Value extent = root.get("extent", "" );
  cout << extent;
  return 0;
}