# Edgars Lakis, 7.10.2023
# Mazais praktiskais darbs - Bin Packing uzdevums.
import random
import math
import time

#Uzkonstruē un atrod sākotnējo risinājumu.
def first_fit_decreasing(items, bins):
    # Kastes (items) tiek sarindotas pēc to izmēriem (garums * platums), lai lielākās kastes ir masīva sākumā
    items.sort(key=lambda item: item[0] * item[1], reverse=True)

    # Uzkonstruē TUKŠAS kravas mašīnas
    bin_count = len(bins)
    bin_contents = [[(0, 0)] for _ in range(bin_count)]  # katrā mašīnā ieliek tukšu 0 x 0 kravu, citādi nestrādā "2. Atrast apkārtni"

    # First Fit Decreasing algoritms pēc kārtas ņem kastes, sākot ar lielāko
    for item in items:
        # Kasti (item) mēģina ielikt kādā no pieejamajām kravām (bins[i]), ņemot vērā kravas izmēra ierobežojumu
        for i in range(bin_count):
            # Pirmās iekavas - mašīnā jau esošās kravas summa. Otrās - tekošā kaste. Trešās - kravas izmēra ierobežojums
            if (sum(w * l for w, l in bin_contents[i]) + (item[0] * item[1]) <= (bins[i][0] * bins[i][1])):
                # Ja ir vieta tekošajai kastei, tad to pievieno i-tajā kravā
                bin_contents[i].append(item)
                break
        else:
            print("Kastei nav vietas nevienā no kravas mašīnām")
    # Sākotnējais risinājums
    return bin_contents

# Izmaksu funkcija. Aprēķina kravas mašīnu aizpildījumu
def calculate_total_size(bin_contents):
    return [sum(w * l for w, l in bin) for bin in bin_contents]

# Izmaksu funkcijas vērtība ir tas, 
def calculate_cost(bin_contents):
    total_sizes = calculate_total_size(bin_contents)
    return max(total_sizes)


def simulated_annealing(initial_solution, TEMPERATURE, T_STEP, bins):
    current_solution = initial_solution
    current_cost = calculate_cost(current_solution)

    best_solution = current_solution
    best_cost = current_cost
    running_cost = [] #masīvs, kurā novēros izmaksu optimizāciju ar katrā algoritma iterācijā
    for _ in range(L):
        T = TEMPERATURE
        while T > 0.1: #CIKLS (skatīt komentāru par T cikla beigās). Apstāšanās kritērijs - temperatūra sasniedz 0.1
            # 2. Atrast apkārtni - iegūst nejaušus kaimiņus. Tādā veidā izvēlas nākošā risinājuma kandidātu no apkārtnes nejauši mainot divas kastes vietām
            neighbor_solution = current_solution.copy()
            bin1 = random.randint(0, len(neighbor_solution) - 1)
            bin2 = random.randint(0, len(neighbor_solution) - 1)
            item1 = random.randint(0, len(neighbor_solution[bin1]) - 1)
            item2 = random.randint(0, len(neighbor_solution[bin2]) - 1)
            
            # Samainam vietām divas kastes:
            neighbor_solution[bin1][item1], neighbor_solution[bin2][item2] = neighbor_solution[bin2][item2], neighbor_solution[bin1][item1]
            
            # Aprēķinām izvēlētā risinājuma izmaksas un starpību starp līdz šim labākā risinājuma izmaksām (delta)
            neighbor_cost = calculate_cost(neighbor_solution)
            delta_cost = neighbor_cost - current_cost
            
            # 3. Novērtē apkārtni. Ja labāks par redzeto (izmaksu starpība (delta) ir negatīva) VAI labāks par metamā kauliņā random.
            # Varbūtība akceptēt sliktāku risinājumu (random < exp) zemā temperatūrā samazinās. Tāpat, ja liela izmaksu starpība.
            if delta_cost < 0 or random.random() < math.exp(-delta_cost / T):
                current_solution = neighbor_solution
                current_cost = neighbor_cost
            # 4. Pasludinām jaunatrasto risnājumu par līdz šim labāko risinājumu, ja tā izmaksas ir mazākas.
            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost # Piefiksējām jaunatrasta risinājuma izmaksas
            running_cost.append(best_cost) # Uzlabotās izmaksas piefiksē, lai sekotu līdzi risinājuma kvalitātei.
            # 5. Izvēlas nākošo risinājumu, mainot TEMPERATŪRAS slieksni (lineāra mainīšana)
            T *= T_STEP
            # Turpina CIKLU līdz izpildās apstāšanās kritērijs - temperatūra samazinās no 1 līdz 0.1 ar soli T_STEP (0.05)
    return best_solution, running_cost


def print_bins(bin_contents):
    for i, bin in enumerate(bin_contents):
        print(
            f"Kravas mašīnā '{i + 1}' sakrautas {len(bin)} kastes izmantojot laukumu {sum(w * l for w, l in bin)}: {bin}")


if __name__ == "__main__":
    # Domēna definēšana, vienumi un to atkarības.
    # Šeit aprakstu datu struktūru problēmas risinājumam.
    # Risinājums ir mašīnai piekārtotas kravas kastes. Kastes (items) aparaksta plānošanas vērtību kopu.
    # Testēšanas piemēri:
    # items = [(7, 2), (1, 3), (4, 2), (2, 1), (2, 1), (1, 3), 
    #          (7, 3), (4, 1), (8, 2), (1, 3), (8, 2), (1, 3), (4, 2)]
    # bins = [(4, 5), (4, 5), (4, 5), (4, 5), (4, 5), (4, 5)]

    items = []
    bins = []
    n = 12 # kravas kastu skaits
    m = 5 # kravas mašīnu skaits
    for _ in range(n):
        i = random.randint(1,5)
        items.append((i,i))
    for _ in range(m):
        j = random.randint(1,10) 
        bins.append((j,j))
    print("Items:", items)
    print("Bins:", bins)

    # konstantes optimizācijai ar Simulated Annealing
    TEMPERATURE = 1000
    T_STEP = 0.95
    # Iterāciju skaits
    L = 1

    start = time.time()
    # Solve the Bin Packing Problem using First Fit Decreasing
    bin_contents = first_fit_decreasing(items, bins)
    print("Sākotnējais risinājums:", bin_contents)
        
    # Optimālā atrisinājuma instance
    optimized_solution, running_cost = simulated_annealing(bin_contents, TEMPERATURE, T_STEP, bins)
    end = time.time()
    # Print the bins
    print_bins(optimized_solution)
    print("Izmaksas katrā iterācijā:", running_cost)
    print(end-start)