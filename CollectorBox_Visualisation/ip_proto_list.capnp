#@0x934efea7f017fff0;
@0x8bf19c04cd8345d7;
#@0x934efea7f017fff0;
struct IPAddress{
   id @0 :UInt32;
   addr @1: Text;

}

struct FlowIn{
        # TODO(abhishek): convert ips into int32?
        srcip @0 : Text;
        srcport @1 : UInt32;
        dstip @2 : Text;
        dstport @3 : UInt32;
        protoc @4 : Text;
}

interface Flowtransmit{

  #src @0 (srcip :Text) -> ();
  #src @0 (databrick: List(UInt32), hitters: List(Lidatabrick)) -> (value: Float64);
  src @0 (databrick: List(UInt32), hitters: List(Lidatabrick)) -> (srcbins: List(UInt32), dstbins: List(UInt32)); # new visualization uses lists
  #src @0 (port :Int32, srcip: Text, dbk1: List(Sbk1), databrick: List(Lidatabrick)) -> (value: Float64);
  #srcport @1 : UInt32;
}
struct Sbk1{

  intensity@0 : Int32;
}

struct Lidatabrick{


  #dbk @0 :Int32;
  ipsrc @0:Text;
  ipdst @1 :Text;
  bytes @2 :Int32;
}
