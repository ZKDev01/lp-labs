package main

import (
	"fmt"
	"math/rand"
	"time"
)

/*
============================================================================
SOLUCIÓN: Usando Canales
- Usa canales con buffer para representar los tenedores
- Cada tenedor es un canal que puede contener un valor booleano
- Los filósofos toman tenedores recibiendo del canal y los devuelven enviando al canal
- Para evitar deadlocks, se usa un timeout al intentar tomar los tenedores
============================================================================
*/

// Estructura para representar un filósofo usando channels
type PhilosopherChannels struct {
	id        int
	leftFork  chan bool
	rightFork chan bool
	done      chan bool
}

func (p *PhilosopherChannels) dine() {
	eaten := 0
	for eaten < 3 {
		p.think()
		if p.eat() {
			eaten++
		}
	}
	p.done <- true
}

func (p *PhilosopherChannels) think() {
	fmt.Printf("Filósofo %d está pensando...\n", p.id)
	time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
}

func (p *PhilosopherChannels) eat() bool {
	fmt.Printf("Filósofo %d intenta tomar los tenedores\n", p.id)
	timeout := time.After(500 * time.Millisecond)

	// Intentar tomar el tenedor izquierdo
	select {
	case <-p.leftFork:
		fmt.Printf("Filósofo %d tomó el tenedor izquierdo\n", p.id)
	default:
		fmt.Printf("Filósofo %d no pudo tomar el tenedor izquierdo, vuelve a pensar\n", p.id)
		return false
	}

	// Intentar tomar el tenedor derecho con timeout
	select {
	case <-p.rightFork:
		fmt.Printf("Filósofo %d tomó el tenedor derecho\n", p.id)
	case <-timeout:
		fmt.Printf("Filósofo %d no pudo tomar el tenedor derecho a tiempo, suelta el izquierdo y vuelve a pensar\n", p.id)
		p.leftFork <- true
		return false
	}

	// Comer durante un tiempo aleatorio (entre 0 y 999 ms)
	fmt.Printf("Filósofo %d está comiendo...\n", p.id)
	time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)

	// Devolver tenedores
	p.leftFork <- true
	p.rightFork <- true
	fmt.Printf("Filósofo %d terminó de comer y devolvió los tenedores\n", p.id)
	return true
}

func solutionWithChannelsOnly(numPhilosophers int) {
	fmt.Println("SOLUCIÓN: CHANNELS")
	
	// Crear channels para los tenedores  
	forks := make([]chan bool, numPhilosophers)
	for i := 0; i < numPhilosophers; i++ {
		forks[i] = make(chan bool, 1)
		forks[i] <- true // Inicializar cada tenedor como disponible
	}
	
	// Crear channels para señalar cuando cada filósofo termine
	done := make([]chan bool, numPhilosophers)
	for i := 0; i < numPhilosophers; i++ {
		done[i] = make(chan bool)
	}
	
	// Crear y lanzar filósofos
	philosophers := make([]*PhilosopherChannels, numPhilosophers)
	for i := 0; i < numPhilosophers; i++ {
		philosophers[i] = &PhilosopherChannels{
			id:        i,
			leftFork:  forks[i],
			rightFork: forks[(i+1)%numPhilosophers],
			done:      done[i],
		}
		go philosophers[i].dine()
	}
	
	// Esperar a que todos terminen
	for i := 0; i < numPhilosophers; i++ {
		<-done[i]
	}
	
	fmt.Println("Todos los filósofos terminaron de cenar")
	fmt.Println()
}

func main() {
	solutionWithChannelsOnly(5)
}