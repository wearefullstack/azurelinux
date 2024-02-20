package pedantic

import (
	"fmt"
	"testing"
)

var testError = fmt.Errorf("test error")

func TestEnablePedanticMode(t *testing.T) {
	EnablePedanticMode(true)
	if !IsPedanticModeEnabled() {
		t.Errorf("Expected pedantic mode to be enabled")
	}
	EnablePedanticMode(false)
	if IsPedanticModeEnabled() {
		t.Errorf("Expected pedantic mode to be disabled")
	}
}

func TestPedanticError(t *testing.T) {
	EnablePedanticMode(true)
	// Make sure nil is ok
	err := PedanticError(nil)
	if err != nil {
		t.Errorf("Expected no error")
	}
	// Should get error still
	err = PedanticError(testError)
	if err != testError {
		t.Errorf("Expected pedantic error")
	}
	EnablePedanticMode(false)
	err = PedanticError(nil)
	if err != nil {
		t.Errorf("Expected no error")
	}
	err = PedanticError(testError)
	if err != nil {
		t.Errorf("Expected no error")
	}
}
