# Kravas automašīnu aizpildīšana ar kastēm (bin packing). Mazais praktiskais darbs
Edgars Laķis
7.10.2023
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
  - kravas kastu masīvs (items) ar atsevišķām kastēm (item)
  - mašīnu piepildījuma struktūra apkopota masīvā bin_contents
  - sakrautās kravas izmērs glabājas total_sizes
Plānošanas mainīgo kopa šajā uzdevumā ir m kravas automašīnas un n kastes ar piekārtotu garumu un platumu. Galvenais ierobežojums meklēšanas telpā ir kravas mašīnas izmērs 2D, respektīvi, kravas mašīnā nevar ielikt vairāk kravu, kā to ļauj mašīnas izmērs 2D.
### Novērtēšana
Risinājums ir mašīnai piekārtotas kravas kastes. Risinājuma novērtēšana tiek veikta, saskaitot kravas kastu kopējo izmēru katrā mašīnā. Jo mazāk mašīnās var satilpināt visas kastes, jo optimālāks risinājums. Izmaksu funkcija atgriež piepildītākās kravas mašīnas aizpildījumu (max). Par labāku risinājumu tiek uzskatīts arī vienmērīgāk sadalītas kastes starp mašīnām, respektīvi, mazāk "pārbāztas" mašīnas.
Tālāk aprēķina izvēlētā risinājuma izmaksas un starpību starp līdz šim labākā risinājuma izmaksām (delta). Ja labāks par redzeto (izmaksu starpība (delta) ir negatīva) VAI metot kauliņu. Varbūtība akceptēt sliktāku risinājumu (random < exp) zemā temperatūrā samazinās. Varbūtība samazinās arī, ja liela izmaksu starpība (delta).
Beigās pasludinām jaunatrasto risnājumu par līdz šim labāko risinājumu, ja tā izmaksas ir mazākas par iepriekšējo.
### Gājiens
Gājienā izvēlas nejaušu kastu pāri (kaimiņus) no visu mašīnu masīva. Kaimiņu pāri var veidot kastes gan no vienas mašīnas, gan no dažādām mašīnām. Izvēlēto kastu pāri samaina vietām. Tālāk rēķina (novērtē) šo jauno kravu sadalījumu pa mašīnām. Nākamais gājiens sākas ar samazinātu temperatūras (ar noteiktu 5% soli).
Šāds gājiens tiek atkārtots L reizes (iterācijas).
## Testēšanas apraksts
Testēt iespējams norādot automašīnu skaitu m un kravas kastes n.
Sākotnēji testēju ar manuāli ievadītām kravas kastēm un mašīnām.
### Izpildes laiks
Optimizācijas algoritma izpilde prasa 3..5 milisekundes ar vienu iterāciju. Desmit iterācijām - 15..16 milisekundes.
### Risinājuma kvalitāte
Par optimumu varētu uzskatīt vienmērīg izkārtotu kravu pa iespējami maz mašīnām. Novēroju, ka minimālais mašīnu skaits tiek sasniegts jau ar First Fit Decreasing algoritmu. Simmulated Anealing uzlabo kravas izkārtojumu to vienmērīgojot.