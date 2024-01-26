#lang racket

(define input_lines
  (file->lines "test-1.txt"))


(set! input_lines
  (map 
    (lambda (line)
      (map
        (lambda (part)
          (string-trim part))
      (string-split line "|")))
    input_lines))

(define get_strings_with_length 
  (lambda (strings length)
    (filter 
      (lambda (x)
        (eq? (string-length x) length))
      strings)))

(define get_key_with_value 
  (lambda (h value)
    (car (filter
      (lambda (x)
        (eq? (cdr x) value))
      (hash->list h)))))

; f = it's the only char that is in every line except one
; c = find 1 & 4 and c is the one they share that isn't f
; a = find 7 and a is whatever char remains besides c & f
; d = find 4 and all length 5 chars and the char they share is d
; b = find all length 5 and whatever char they don't have in common is b
; g = find all lenght 6 for each remove all f,c,a,d,b and for the remaining 
;     chars that has length 1 (9) that char is g
; e = find 8 remove all the other found chars and remaining is e
; (define segment_mapping 
;   (make-hash (map cons '("a" "b" "c" "d" "e" "f" "g") '("" "" "" "" "" "" ""))))


(define find_f
  (lambda (line)
    (let ([
           count_keeper (make-hash (map cons '("a" "b" "c" "d" "e" "f" "g") '(0 0 0 0 0 0 0)))
           ])
      (for-each 
        (lambda (input)
          (for-each 
            (lambda (c)
              (hash-set! count_keeper c (+ 1 (hash-ref count_keeper c))))
            (map string (string->list input))))
        (string-split (car line)))
      (car (get_key_with_value count_keeper 9)))))

; (hash-set! segment_mapping "f"
;   (find_f (car input_lines)))

(define find_c
  (lambda (part segments)
    ; find 1 (len = 2) remove "f" and the other is c
    (car(filter
      (lambda (x) (not (string=? (hash-ref segments "f") x)))
      (map string (string->list 
                    (car (get_strings_with_length part 2))))))))

; (hash-set! segment_mapping "c"
;   (find_c (string-split (car (car input_lines))) segment_mapping))

(define find_a 
  (lambda (part segments)
    ; find 7 (len = 3) remove "c" and "f" the remaining is c
    (car (filter
      (lambda (x) 
        (not 
          (or
            (string=? (hash-ref segments "c") x)
            (string=? (hash-ref segments "f") x))))
      (map string (string->list 
                    (car (get_strings_with_length part 3))))))))

; (hash-set! segment_mapping "a"
;   (find_a (string-split (car (car input_lines))) segment_mapping))


; d = find 4 and all length 5 chars and the char they share is d
(define find_d
  (lambda (part)
    (let ([
           count_keeper (make-hash (map cons '("a" "b" "c" "d" "e" "f" "g") '(0 0 0 0 0 0 0)))])
      (for-each
        (lambda (x)
          (for-each 
            (lambda (y)
              (hash-set! count_keeper y (+ 1 (hash-ref count_keeper y))))
            (map string (string->list x))))
        (append (get_strings_with_length part 5) (get_strings_with_length part 4)))
      (car (get_key_with_value count_keeper 4)))))


; (hash-set! segment_mapping "d"
;   (find_d (string-split (car (car input_lines)))))

; b = find all length 5 and whatever char they have in common is b
(define find_b
  (lambda (part)
    (let ([
           count_keeper (make-hash (map cons '("a" "b" "c" "d" "e" "f" "g") '(0 0 0 0 0 0 0)))])
      (for-each
        (lambda (x)
          (for-each 
            (lambda (y)
              (hash-set! count_keeper y (+ 1 (hash-ref count_keeper y))))
            (map string (string->list x))))
        (get_strings_with_length part 5))
      (car (get_key_with_value count_keeper 1)))))

; (hash-set! segment_mapping "b"
;   (find_b (string-split (car (car input_lines)))))

; g = find all lenght 6 for each remove all f,c,a,d,b and for the remaining 
;     chars that has length 1 (9) that char is g

(define find_g
  (lambda (part segments)
    (let (
           [found_segments (filter non-empty-string? (hash-values segments))])
      (println found_segments)
      (println (get_strings_with_length part 6))
      (caar (filter 
        (lambda (x) (eq? (length x) 1))
        (map
          (lambda (x)
            (filter
              (lambda (y)
               (not (member y found_segments)))
              (map string (string->list x))))
          (get_strings_with_length part 6)))))))


; (hash-set! segment_mapping "g"
;   (find_g (string-split (car (car input_lines))) segment_mapping))

; e = find 8 remove all the other found chars and remaining is e
(define find_e
  (lambda (part segments)
    (let (
           [found_segments (filter non-empty-string? (hash-values segments))])
      (caar (filter 
        (lambda (x) (eq? (length x) 1))
        (map
          (lambda (x)
            (filter
              (lambda (y)
               (not (member y found_segments)))
              (map string (string->list x))))
          (get_strings_with_length part 7)))))))

; (hash-set! segment_mapping "e"
;   (find_e (string-split (car (car input_lines))) segment_mapping))

; f = it's the only char that is in every line except one
; c = find 1 & 4 and c is the one they share that isn't f
; a = find 7 and a is whatever char remains besides c & f
; d = find 4 and all length 5 chars and the char they share is d
; b = find all length 5 and whatever char they don't have in common is b
; g = find all length 6 for each remove all f,c,a,d,b and for the remaining 
;     chars that has length 1 (9) that char is g
; e = find 8 remove all the other found chars and remaining is e

(define set_letter
  (lambda (letter output mapping)
    (hash-set! mapping letter output)))

(for-each
  (lambda (line)
    (let ( 
           [segment_mapping (make-hash (map cons '("a" "b" "c" "d" "e" "f" "g") '("" "" "" "" "" "" "")))]
           [line_input (string-split (car line))]
           [line_output (string-split (car (cdr line)))])
      (set_letter "f" (find_f line) segment_mapping)
      (set_letter "c" (find_c line_input segment_mapping) segment_mapping)
      (set_letter "a" (find_a line_input segment_mapping) segment_mapping)
      (set_letter "d" (find_d line_input) segment_mapping)
      (set_letter "b" (find_b line_input) segment_mapping)
      (set_letter "g" (find_g line_input segment_mapping) segment_mapping)
      ; (set_letter "e" (find_e line_input segment_mapping) segment_mapping)
      (println segment_mapping)))
  input_lines)

; (println segment_mapping)
