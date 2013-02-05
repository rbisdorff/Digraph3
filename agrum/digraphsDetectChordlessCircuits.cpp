/* ------------------------------------------------*
   digraphsDetectChordlessCircuits.cpp
  
   with agrum library
   optimised with visited P2s marking.
   without unicity test.
   
   compile with
   g++ -Wall -O4 digraphsEnumChordlessCircuits.cpp -o enumChordlessCircuits -lagrum
            [-I$InstallDir/trunk/src] if working on a Mac XOs
   
   Takes ttwo STRING arguments: 
   1) an input file with a list of arcs: n1 n2 per line 
   2) an output filename (general a NamedTemporaryFile instance)
   
   RB August 2011 
 * ----------------------------------------------- */

#include <iostream>
#include <cstdlib>
#include <stdio.h>
#include <ctime>
#include <fstream>
#include <assert.h>
#include <agrum/graphs/diGraph.h>

using namespace std;
using namespace gum;

// #define SAMPLESIZE 1
// #define ORDER 50
// #define CUTLEVEL 50

// double diffclock(const clock_t clock1,const clock_t clock2)
// {
//  double diffticks=clock1-clock2;
//  double diffms=diffticks/CLOCKS_PER_SEC;
//  return diffms;
// }

bool chordlessPath(DiGraph &g, 
		  List<NodeId> &Ln,
		  const NodeId n2, 
		  List< List<NodeId> > &Lf, 
		   Set<Arc> &visitedArcs
		  ){
  // recursive version ...
  // g  : Digraph instance (global)
  // Ln,L : lists of nodes of the current chordless path in construction (global, local)
  // n2 : end node of the path
  // Lf : list of all chordless paths found so far (global)
  // visitedArcs : set of already visited arcs (global)
  
  NodeId n1 = Ln.back();
  bool detectChordlessPath = false;
  
  visitedArcs.insert(Arc(n1,n2));
  visitedArcs.insert(Arc(n2,n1));

  if (g.existsArc(n1,n2) and not(g.existsArc(n2,n1))) {
    // If there exists an asymmetric path from node n1 to node n2 
    Ln.pushBack(n2);
    // clog << "Ln: " << Ln << endl;
    // cout << "Ln" << Ln << endl;
    Lf.insert(Ln);
    detectChordlessPath = true;
    return detectChordlessPath;
  }
  else {
    if (!detectChordlessPath){

      // Otherwise we consider all immediate asymmetric successor nodes of n1
      const Set<NodeId>& children=g.children( n1 );
      const Set<NodeId>& parents=g.parents( n1 );
      Set<NodeId>  b;
      b = children - parents;
      // clog << "b : " << b << ", " << children << ", " << parents << endl;
      for ( SetIterator<NodeId> nodeIt = b.begin( ); nodeIt != b.end(); ++nodeIt ) {
	// clog << " nodeIt -->>" << *nodeIt << endl;
	const Arc arc = Arc(n1,*nodeIt);
	if (!visitedArcs.contains(arc)){
	  NodeId n = arc.head();
	  List<NodeId> L = Ln; // make local copy of the current chordless path Ln
	  // clog << "L: " << L << ", n: " << n << endl;
	  // We have to verify that node n does not create a chord
	  int Chord = 0;
	  for ( List<NodeId>::iterator i = L.begin( ); i != L.end(); ++i ) {
	    NodeId x = *i;
	    // clog << n << " --> " << x << " ? " << endl; 
	    if (x == n1) {
	      if (g.existsArc(n,x)) Chord = 1;
	    } 
	    else {
	      if (x == n2) {
		if (g.existsArc(x,n)) Chord = 1;
	      } else {
		if (g.existsArc(n,x) || g.existsArc(x,n)) Chord = 1;
	      }
	    }
	  }
	  // I n does not create a chord we continue with the recursion
	  if (Chord < 1) {
	    L.insert(n);
	    if (chordlessPath(g,L,n2,Lf,visitedArcs)) {
		detectChordlessPath = true;
		break;
	    }	    
	  }
	  // and we consider the next asymmetric children of n1
	}
      }    
    };
  }
    return detectChordlessPath;
}

//-------------------------

int main(int argc, char* argv[]){
 
 assert(argc == 3);

 // determine the order of the input digraph
 
 ifstream in(argv[1]);
 assert(in);
 int order = 0;
 char an1[256];
 char an2[256];
 int n1;
 int n2;
 while (in.good()) {
   in >> an1 >> an2;
   // cout << an1 << " " << an2 << endl;
   n1 = atoi(an1);
   n2 = atoi(an2);
   if (n1 > order) { order = n1;};
   if (n2 > order) { order = n2;};
 }
 // cout << "order = " << order << endl;
 in.close();


 // creating empty graphs
 DiGraph g1;
 // adding nodes to g1
 int nn = order + 1;
 for (int i = 1; i < nn; ++i){
   NodeId in = i; 
   g1.insertNode(in);
 }

 // initialize the arcs
 in.open(argv[1]);
 int i = 0;
 NodeId initialNode;
 NodeId terminalNode;
 in >> an1 >> an2;
 while (in.good()) {
   n1 = atoi(an1);
   n2 = atoi(an2);
   initialNode = n1;
   terminalNode = n2;
   // cout << initialNode << " " << terminalNode << endl;
   g1.insertArc(initialNode,terminalNode);
   i++;
   in >> an1 >> an2;
 }
 in.close();
 // cout << "number of arcs added = " << i << endl; 
 // float arcDensity = float(i) / float(order * (order - 1));
 // cout << "arc density = " << arcDensity << endl;
 
 
 // show all chordless circuits
 // cout << endl << endl << "*Show all chordless circuits*" << endl;
 // clock_t cstart,cend;
 // time_t start,end;
 // cstart=clock();
 // time(&start);

 List< List<NodeId> > chordlessCircuitsList;
 Set<Arc> visitedArcs;
 
 for ( DiGraph::NodeIterator i = g1.beginNodes(); i != g1.endNodes(); ++i ){
   // clog << " ===>>> Starting from " << *i << " ? : " << endl;
   // cout << " ===>>> Starting from " << *i << " ? : " << endl;
   NodeId v = *i;
   List<NodeId> Path;
   Path.insert(v);
   List< List<NodeId> > vCC;
   if (chordlessPath(g1,Path,v,vCC,visitedArcs)){
     for ( List< List<NodeId> >::iterator i = vCC.begin( ); i != vCC.end(); ++i ) {
       List<NodeId> cur = *i;
       chordlessCircuitsList.insert(cur);};
     break;
   };
   
  };
 // cend=clock();
 // time(&end);
 // clog << chordlessCircuitsList.size() << " circuit(s): " << chordlessCircuitsList.toString() << endl;
 // double diff = difftime(end,start);
 // double cdiff = diffclock(cend,cstart);
 // cout << chordlessCircuitsList.size() << ", " << diff << endl;
 // cout << "Number of chordless circuits : " << chordlessCircuitsList.size() << endl;
 // cout << "Execution time: " << cstart-cend << " sec." << endl;
 // cout << "with C++/Agrum, R Bisdorff, August 2011 " << endl;
 
 // write a Python list named circuitsList gathering the circuits detected
 ofstream out(argv[2]);
 assert(out); 

 // unsigned int x[order];
 // for (int ii =0; ii<order; ii++) x[ii] = 0;  // Initialize
 out << "circuitsList = [" << endl;
 for (List< List<NodeId> >::iterator c = chordlessCircuitsList.begin();c != chordlessCircuitsList.end(); ++c){
   List<NodeId> circuit = *c;
   out << "[ ";
   for (List<NodeId>::iterator ino = circuit.begin(); ino != circuit.end(); ++ino){
     NodeId node = *ino;
     out << node << ", ";
   }
   out << " ]," << endl;
   // out << circuit << endl;
 }
 out << "]";
 out.close();
 
}
