#include<iostream>
#include <vector>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <fstream>
#include <sstream>

using namespace std;

struct Process{
    string name;
    unsigned int arrival;
    unsigned int memory_req;
    unsigned int exe_time;
    unsigned int counter;
};

struct Processor{
    vector <Process> queue;
    vector <Process> executing;
    unsigned int Total_Memory;
};

void leerFich(string file, vector<Process> &process){
    ifstream namefile(file);
    if(namefile.is_open()){
        string linea;
        while(getline(namefile, linea)){
            stringstream sss(linea);
            Process processs;
            sss >> processs.name;
            sss >> processs.arrival;
            sss >> processs.memory_req;
            sss >> processs.exe_time;
            processs.counter = processs.exe_time;
            if(processs.memory_req>=100&&processs.memory_req<=2000)
                process.push_back(processs);
        }
        namefile.close(); 
    }
    else
        cout<< "The input file is not found in the directory" << endl;
}

void ampliarProcessor(Processor &processor, int pos, int memoriaRestante){
    Process new_gap;
    new_gap.name = "hueco";
    new_gap.arrival = 0;
    new_gap.counter = 0;
    new_gap.exe_time = 0;
    new_gap.memory_req = memoriaRestante;
    processor.executing.push_back(new_gap);
	for(int x = processor.executing.size() - 1 ; x > pos + 1; x--)
   		swap(processor.executing[x], processor.executing[x-1]);
}

void eliminarProcess(vector<Process> &executing){
    for(int y = executing.size() - 1; y >= 0 ; y--){
    	if(executing[y].name.compare("hueco") != 0)
        	executing[y].counter--;
        if(executing[y].counter == 0)
            executing[y].name = "hueco";
    }
}

bool controlTiempo(vector<Process> queue, vector<Process> executing, int Total_Memory){
    bool count = false;
    if(queue.empty()){
        for(int x = 0; x < (int)executing.size() && count == false; x++){
            if(executing[x].counter != 0)
                count = true;
        }
        if(executing[0].name.compare("hueco") == 0 && executing[0].memory_req == (unsigned int) Total_Memory)
        	count = false;
    }
    else
        count = true;
    return count;
}

void solaparHuecos(vector<Process> &executing){
    for(int x = (int) executing.size() -1; x >= 0; x--){
        if(x < (int) executing.size()  - 1 &&  executing[x].name.compare("hueco") == 0 && executing[x+1].name.compare("hueco") == 0){
            executing[x].memory_req += executing[x+1].memory_req;
            executing.erase(executing.begin() + x + 1);
        }
    }
}

void queueToProcessor(Processor &processor, bool &erased){
	int hueco = -1;
    for(int x=0; x < (int) processor.executing.size() && erased == false; x++){
        if(processor.executing[x].name.compare("hueco") == 0 && processor.queue[0].memory_req <= processor.executing[x].memory_req){
            hueco = x;
            int memoriaRestante = processor.executing[x].memory_req - processor.queue[0].memory_req;
            if( memoriaRestante == 0)
                swap(processor.executing[x], processor.queue[0]);
            else{
				ampliarProcessor(processor, x, memoriaRestante);
                swap(processor.executing[x], processor.queue[0]);
				solaparHuecos(processor.executing);
            }
            processor.queue.erase(processor.queue.begin());	
            erased = true;
        }
    }
    if(hueco == -1)
            	erased = false;
}

void ProcessToProcessor(vector<Process> &process, Processor &processor){
	int posHueco = -1;
    for(int x=0; x < (int) processor.executing.size(); x++){
        if(processor.executing[x].name.compare("hueco") == 0 && process[0].memory_req <= processor.executing[x].memory_req){
        	posHueco = x;
            int memoriaRestante = processor.executing[x].memory_req - process[0].memory_req;
            if( memoriaRestante == 0)
                swap(processor.executing[x], process[0]);
            else{
				ampliarProcessor(processor, x, memoriaRestante);
                swap(processor.executing[x], process[0]);
				solaparHuecos(processor.executing);
            }	
        }
    }
    if(posHueco == -1){
        processor.queue.push_back(process[0]);
    }
	process.erase(process.begin());
}

void grafica(Processor processor){
    for(int x=0; x < (int) processor.executing.size(); x++){
        cout << "************************************" << endl;
        int temp=processor.executing[x].memory_req/50;
        for(int j=0; j < temp; j++){
            if(j==temp/2 && processor.executing[x].memory_req<1000){
                if(processor.executing[x].name.size()==2)
                    cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"                *"<<endl;
                else{
                    if(processor.executing[x].name.size()==3)
                        cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"               *"<<endl;
                    else{
                        if(processor.executing[x].name.size()==4)
                            cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"              *"<<endl;
                        else{
                            if(processor.executing[x].name.size()==5)
                                cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"             *"<<endl;
                            else{
                                if(processor.executing[x].name.size()==5)
                                    cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"             *"<<endl;
                                else
                                    cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"             *"<<endl;
                            }
                        }
                    }
                }
            }
            else{ 
                if(j==temp/2 && processor.executing[x].memory_req>=1000)
                    cout << "*            "<<processor.executing[x].name << " " << processor.executing[x].memory_req<<"            *"<<endl;
                else
                    cout << "*                                  *"<<endl;
            }
        }
        cout << "************************************" << endl;
    }
    cin.get();
}

void algPeorHueco(int Total_Memory, string name_Import, string name_Export){
    vector<Process> process;
    leerFich(name_Import, process);
    Processor processor;
    processor.Total_Memory = (unsigned int) Total_Memory;
    Process initialization;
    initialization.name = "hueco";
    initialization.arrival = 0;
    initialization.counter = 0;
    initialization.exe_time = 0;
    initialization.memory_req = Total_Memory;
    processor.executing.push_back(initialization);
    bool count = true;
    ofstream namefile(name_Export);
    if(namefile.is_open()){
		for(int instante = 1; count == true || !process.empty(); instante++){
            cout << "Instant " << instante << ": "<< endl;
       		namefile << instante << " ";
		    bool erased;
		    do{
		    	erased = false;
		        if( !processor.queue.empty() && (processor.queue[0].memory_req > processor.Total_Memory)){
		            processor.queue.erase(processor.queue.begin());
		            erased = true;
		        }
		        else if (!processor.queue.empty())
					queueToProcessor(processor, erased);
		    }while(erased == true);
		    while(!process.empty() && (int)process[0].arrival == instante){
		    	int posHueco = -1;
		    	int diferencia = -1;
			    for(int x=0; x < (int) processor.executing.size(); x++){
			        if(processor.executing[x].name.compare("hueco") == 0 && process[0].memory_req <= processor.executing[x].memory_req){
			        	if((unsigned)diferencia < processor.executing[x].memory_req - process[0].memory_req || diferencia == -1){
				        	posHueco = x;
				        	diferencia = processor.executing[x].memory_req - process[0].memory_req;	
						}
			        }
			    }
			    if(posHueco == -1)
			        processor.queue.push_back(process[0]);
				else{
		            if( diferencia == 0)
		                swap(processor.executing[posHueco], process[0]);
		            else{
						ampliarProcessor(processor, posHueco, diferencia);
		                swap(processor.executing[posHueco], process[0]);
						solaparHuecos(processor.executing);
		            }	
				}
				process.erase(process.begin()); 			    	
		    }
			int posInicial = 0;
		    for(int x = 0; x < (int)processor.executing.size(); x++){
		        namefile << "[" << posInicial << " " << processor.executing[x].name << " " << processor.executing[x].memory_req << "] ";
		        posInicial += processor.executing[x].memory_req;
		    }
            grafica(processor);
			cout << endl;
			namefile << endl;
			count = controlTiempo(processor.queue, processor.executing, Total_Memory);
		    eliminarProcess(processor.executing);
		    solaparHuecos(processor.executing);
		}
        namefile.close();
    }
    else
        cout << "The output file could not be created" << endl;
    cout << "Finished algorithm" << endl;
}

void algMejorHueco(int Total_Memory, string name_Import, string name_Export){
	vector<Process> process;
    leerFich(name_Import, process);
    Processor processor;
    processor.Total_Memory = (unsigned int) Total_Memory;
    Process initialization;
    initialization.name = "hueco";
    initialization.arrival = 0;
    initialization.counter = 0;
    initialization.exe_time = 0;
    initialization.memory_req = Total_Memory;
    processor.executing.push_back(initialization);
    bool count = true;
    ofstream namefile(name_Export);
    if(namefile.is_open()){
		for(int instante = 1; count == true || !process.empty(); instante++){
            cout << "Instant " << instante << ": "<< endl;
       		namefile << instante << " ";
		    bool erased;
		    do{
		    	erased = false;
		        if( !processor.queue.empty() && (processor.queue[0].memory_req > processor.Total_Memory)){
		            processor.queue.erase(processor.queue.begin());
		            erased = true;
		        }
		        else if (!processor.queue.empty())
					queueToProcessor(processor, erased);
		    }while(erased == true);
		    while(!process.empty() && (int)process[0].arrival == instante){
		    	int posHueco = -1;
		    	int diferencia = -1;
			    for(int x=0; x < (int) processor.executing.size(); x++){
			        if(processor.executing[x].name.compare("hueco") == 0 && process[0].memory_req <= processor.executing[x].memory_req){
			        	if((unsigned)diferencia > processor.executing[x].memory_req - process[0].memory_req || diferencia == -1){
				        	posHueco = x;
				        	diferencia = processor.executing[x].memory_req - process[0].memory_req;	
						}
			        }
			    }
			    if(posHueco == -1)
			        processor.queue.push_back(process[0]);
				else{
		            if( diferencia == 0)
		                swap(processor.executing[posHueco], process[0]);
		            else{
						ampliarProcessor(processor, posHueco, diferencia);
		                swap(processor.executing[posHueco], process[0]);
						solaparHuecos(processor.executing);
		            }	
				}
				process.erase(process.begin()); 			    	
		    }
			int posInicial = 0;
		    for(int x = 0; x < (int)processor.executing.size(); x++){
		        namefile << "[" << posInicial << " " << processor.executing[x].name << " " << processor.executing[x].memory_req << "] ";
		        posInicial += processor.executing[x].memory_req;
		    }
            grafica(processor);
			cout << endl;
			namefile << endl;
			count = controlTiempo(processor.queue, processor.executing, Total_Memory);
		    eliminarProcess(processor.executing);
		    solaparHuecos(processor.executing);
		}
        namefile.close();
    }
    else
        cout << "The output file could not be created" << endl;
    cout << "Finished algorithm" << endl;
}

void inicio(bool &peor_Hueco, bool &mejor_Hueco){
    do{
        int modelo;
        cout<<"1) Press 1 to use the best gap algorithm"<<endl;
        cout<<"2) Press 2 to use the worst gap algorithm"<<endl;
        cout<<"Enter the memory allocation model: ";
        cin>>modelo;
        cin.ignore();
        cout<<endl;
        switch (modelo){
            case 1: 
                mejor_Hueco=true;
                break;
            case 2: 
                peor_Hueco=true;
                break;
            default:
                break;
        }
    }while(peor_Hueco==false && mejor_Hueco==false);
}

int main(int argc, char *argv[]){
    string name_Import = argv[1];
    string name_Export = "Particiones.txt";
    int Total_Memory = 2000;
    bool peor_Hueco = false, mejor_Hueco = false;
    if(argc !=2)
		cout << "You have entered the wrong arguments." << endl;
    else{
        cout << "Chosen input file: " << name_Import << endl 
                << "Chosen dump file: " << name_Export << endl
                << "Maximum processor capacity: " << Total_Memory << endl
                << "=========================================================" << endl;
        cout << "What algorithm do you want to use?" << endl;
        inicio(peor_Hueco, mejor_Hueco);
        if(peor_Hueco == true){
            cout << "You have selected the worst gap algorithm" << endl;
            algPeorHueco(Total_Memory, name_Import, name_Export);
        }
        else{
            cout << "You have selected the best gap algorithm" << endl;
            algMejorHueco(Total_Memory, name_Import, name_Export);
        }
    }
    return 0;
}