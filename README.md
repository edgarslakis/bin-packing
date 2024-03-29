# Kravas automašīnu aizpildīšana ar kastēm (bin packing). Mazais praktiskais darbs
Edgars Laķis
7.10.2023

Saite uz Git(hub) repozitoriju, kas satur programmas kodu:

https://github.com/edgarslakis/bin-packing
## Uzdevuma formulējums 
Dotas m automašīnas, katra ar kravas kastes izmēru w[i] x l[i]. Dotas n kastes ar izmēriem p[j] x g[j]. 
Salikt visas kastes pēc iespējas mazāk automašīnās. Paliekam 2D - kastes nedrīkst likt vienu otrai virsū.

## Algoritma apraksts
1. Konstruējam sākotnējo risinājumu ar First Fit Decreasing heiristiku. 
1. Meklē lokālo minimumu ar Simulated Annealing algoritmu.
1. Kamēr temperatūra nesasniedz pārtraukšanas vērtību (0.1):
   - Izvēlamies jaunu risinājumu ar random seed - kaimiņus
   - Meklē lokālo minimumu
   - Ja atrastais optimums ir labāks par iepriekšējo, tad atceramies to
1. Veicam L iterācijas iepriekšējam solim, katru reizi atiestato temperatūru
1. Labāko atrasto risinājumu pasludinām par galīgo
### Domēns
Domēns sastāv no: 
- Novērtēšanas un izmaksu funkcijas
- Gājiena un apkārtnes funkcijas
- Datu struktūrām, kas apraksta risinājumu:
  - kravas mašīnu masīvs (bins) ar atsevišķām mašīnām (bin) 
  - kravas kastu masīvs (items) ar atsevišķām kastēm (item). No sākuma katrai mašīnai ieliek vienu nulles kravu.
  - mašīnu piepildījuma struktūra apkopota masīvā bin_contents
  - sakrautās kravas izmērs glabājas total_sizes
Plānošanas mainīgo kopa šajā uzdevumā ir m kravas automašīnas un n kastes ar piekārtotu garumu un platumu. Galvenais ierobežojums meklēšanas telpā ir kravas mašīnas izmērs 2D, respektīvi, kravas mašīnā nevar ielikt vairāk kravu, kā to ļauj mašīnas izmērs 2D.
### Arhitektūra
Sākotnēji izmantoju noklusēto Solvera uzstādījumus (ekrānšāviņš). Vien precizējot risināšanas laiku (TerminationConfig().withUnimprovedSecondsSpentLimit) - 10 sekundes. Ar dzeltenu atzīmēts, Akceptors pēc noklusējuma izmanto LateAcceptance, bet Klejotājs (Forager) pasludina pirmo par uzvarētāju. 

### Apkārtnes 
funkciju norāda moveSelector, kurš pēc noklusējuma ir ListChange un ListSwap apvienojums. T.i. Change nodrošina, ka varam nonākt līdz jebkuram risinājumam meklēšanas telpā, un Swap dod paātrinājumu nonākšanai optimumā.
ChangeMove var izvēlēties paciņām piekārtotās (entitySelector) mašīnas no saraksta List<Vehicle vehicleList>, kurš attiecīgi ir anotēts kā @ValueRangeProvider. SwapMove maina vietām paciņas (plānošanas objekti). Pamēģināju arī pillarChangeMoveSelector ar pilāru lielumu no 1 līdz 3, taču risinājums neizdevās sekojošas kļudas dēļ: The selector (DefaultPillarSelector(FromSolutionEntitySelector(Pack))) with randomSelection  (true) and sub pillars does not support getSize() because the number of sub pillars scales exponentially.


Pats darbā pamēģināju pamainīt Solvera noklusēto konfigurāciju SolverConfig.xml failā. Piemērma, Akceptora algoritmu nomainīju no noklusētā Late_Acceptance uz entityTabuSize = 5 un klejotāja (forager) uz acceptedCountLimit = 5. Pamēģināju mainīt entityTabu size uz 3 un 2, tāpāt valueTabuSize. Termination laiku paildzinot desmitkārt nenovēroju risinājuma uzlabošanos. Taču manāms ieguvums bija palielinot klejotāja acceptedCountLimit no 5 uz 20.




### Novērtēšana
Pēc benchmarking var spriest, ka labākais risinājums tiek atrasts ļoti agri un tas vairs neuzlabojas atlikušajā risināšanas laikā. Visticamāk risinājums ir tuvu optimumam. Labāku risinājumu varētu sasniegt ar citiem algoritmiem vai krasi mainot to parametrus.

Vispirms veicu mērogošanas testu, palielinot problēmas mērogu sākot ar 5 paciņām un vienu mašīnu līdz 100 paciņām uz 20 mašīnām. Pie šāda entīšu skaita un piekārtoto atribūtu vērtībām Hardscore ir 0 visos mērogos. Soft_score pieaug līdz ar problēmas mērogu, jo vienkārši pieaug automašīnu skaits (Cost)

Testēju arī veselu BluePrint paneli ar dažādiem Local Search algoritmiem (EVERY_LOCAL_SEARCH_TYPE). Paneļa konfigurācija ir saglabāta BenchmarkConfig.xml failā. Piemērojot katru konfigurāciju dažāda mēroga piemēriem, novēroju, ka visi algoritmi sasniedz praktiski vienādu Best Score. Mērogošanas (Best Score scalability) ziņā mazliet labāks ir HILL_CLIMBING. Tā kā Best Score rādītāji ir līdzīgi, var salīdzināt Worst Score calculation speed differene. Šajā rādītājā VARIABLE_NEIGHBORHOOD_DESCENT, TABU_SEARCH un GREAT_DELUGE ir vājāki.

Apskatīju kādi gājienu tipi (ChangeMove vai SwapMove) dod vislabāko izmaksu samazinājumu, taču atskaitē saņēmu atteikumu: "Graph not available. Either the statistic is not available for this solver configuration, or the benchmark failed."

Risinājums ir mašīnai piekārtotas kravas kastes. Risinājuma novērtēšana tiek veikta, saskaitot kravas kastu kopējo izmēru katrā mašīnā. Jo mazāk mašīnās var satilpināt visas kastes, jo optimālāks risinājums. Izmaksu funkcija atgriež piepildītākās kravas mašīnas aizpildījumu (max). Par labāku risinājumu tiek uzskatīts arī vienmērīgāk sadalītas kastes starp mašīnām, respektīvi, mazāk "pārbāztas" mašīnas.
Tālāk aprēķina izvēlētā risinājuma izmaksas un starpību starp līdz šim labākā risinājuma izmaksām (delta). Ja labāks par redzeto (izmaksu starpība (delta) ir negatīva) VAI metot kauliņu. Varbūtība akceptēt sliktāku risinājumu (random < exp) zemā temperatūrā samazinās. Varbūtība samazinās arī, ja liela izmaksu starpība (delta).
Beigās pasludinām jaunatrasto risnājumu par līdz šim labāko risinājumu, ja tā izmaksas ir mazākas par iepriekšējo.
### Gājiens
Gājienā izvēlas nejaušu kastu pāri (kaimiņus) no visu mašīnu masīva. Kaimiņu pāri var veidot kastes gan no vienas mašīnas, gan no dažādām mašīnām. Izvēlēto kastu pāri samaina vietām. Tālāk rēķina (novērtē) šo jauno kravu sadalījumu pa mašīnām. Nākamais gājiens sākas ar samazinātu temperatūras (ar noteiktu 5% soli).
Šāds gājiens tiek atkārtots L reizes (iterācijas).
## Testēšanas apraksts
Testēt iespējams norādot automašīnu skaitu m un kravas kastes n programmas koda main() funkcijā.
Sākotnēji testēju ar manuāli ievadītu masīvu kravas kastēm un mašīnām. 
### Izpildes laiks
Algoritma izpilde prasa 2..5 milisekundes ar vienu iterāciju. Desmit iterācijām - 15..16 milisekundes.
### Risinājuma kvalitāte
Risinājuma kvalitātei seko līdzi ar massīvu running_cost, kurā pievieno arvien labāka risinājuma izmaksas. Par optimumu varētu uzskatīt vienmērīg izkārtotu kravu pa iespējami maz mašīnām. Novēroju, ka lielākais progress tiek sasniegts jau ar First Fit Decreasing algoritmu. Simmulated Anealing uzlabo kravas izkārtojumu pa mašīnām un to vienmērīgojot.
