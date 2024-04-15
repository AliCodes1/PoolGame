#include <stdio.h>
#include "phylib.h"
#include <stdlib.h>  
#include <string.h>
#include <math.h>  

// Creates a new still ball object with specified number and position.
// Allocates memory for the object and initializes its properties.
// Returns a pointer to the created object or NULL if memory allocation fails.
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    phylib_object *obj = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (obj == NULL) {
        return NULL; // Memory allocation failed
    }
    obj->type = PHYLIB_STILL_BALL;
    
    obj->obj.still_ball.pos = *pos; // Copy position data
    obj->obj.still_ball.number = number;

    return obj;
}


// Creates a new rolling ball object with specified number, position, velocity, and acceleration.
// Allocates memory and initializes the object's properties.
// Returns a pointer to the object or NULL on allocation failure.
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    phylib_object *obj = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (obj == NULL) {
        return NULL; // Memory allocation failed
    }

    obj->type = PHYLIB_ROLLING_BALL;

    obj->obj.rolling_ball.pos = *pos; // Copy position data
    obj->obj.rolling_ball.number = number;
    obj->obj.rolling_ball.vel = *vel;
    obj->obj.rolling_ball.acc = *acc;

    return obj;
}

phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object *obj = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (obj == NULL) {
        return NULL; // Memory allocation failed
    }

    obj->type = PHYLIB_HOLE;
    obj->obj.hole.pos = *pos; // Copy position data
    return obj;
}

phylib_object *phylib_new_hcushion( double y ){
    phylib_object *obj = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (obj == NULL) {
        return NULL; // Memory allocation failed
    }

    obj->type = PHYLIB_HCUSHION;
    obj->obj.hcushion.y = y; // Copy position data
    return obj;
}


phylib_object *phylib_new_vcushion( double x ){
    phylib_object *obj = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (obj == NULL) {
        return NULL; // Memory allocation failed
    }

    obj->type = PHYLIB_VCUSHION;
    obj->obj.vcushion.x = x; // Copy position data
    return obj;
}

// Creates a new table object, initializes its properties, and populates it with default objects (cushions and holes).
// Returns a pointer to the new table or NULL on allocation failure.
phylib_table *phylib_new_table(void){
    phylib_table *table=(phylib_table *)calloc(1,sizeof(phylib_table));
    if(table==NULL){
        return NULL;
    }
    table->time=0.0;
    table->object[0]=phylib_new_hcushion(0.0);
    table->object[1]=phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table->object[2]=phylib_new_vcushion(0.0);
    table->object[3]=phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    
    phylib_coord *hole1Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
    if(hole1Pos==NULL){
        return NULL;
    }
    hole1Pos->x=0;
    hole1Pos->y=0;
    table->object[4]=phylib_new_hole(hole1Pos);
    free(hole1Pos);

    phylib_coord *hole2Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
     if(hole2Pos==NULL){
        return NULL;
    }
    hole2Pos->x=PHYLIB_TABLE_WIDTH;
    hole2Pos->y=0;
    table->object[5]=phylib_new_hole(hole2Pos);
    free(hole2Pos);


    phylib_coord *hole3Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
     if(hole3Pos==NULL){
        return NULL;
    }
    hole3Pos->x=0;
    hole3Pos->y=(PHYLIB_TABLE_LENGTH/2);
    table->object[6]=phylib_new_hole(hole3Pos);
    free(hole3Pos);


    phylib_coord *hole4Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
     if(hole4Pos==NULL){
        return NULL;
    }
    hole4Pos->x=PHYLIB_TABLE_WIDTH;
    hole4Pos->y=(PHYLIB_TABLE_LENGTH/2);
    table->object[7]=phylib_new_hole(hole4Pos);
    free(hole4Pos);

    phylib_coord *hole5Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
     if(hole5Pos==NULL){
        return NULL;
    }
    hole5Pos->x=0;
    hole5Pos->y=PHYLIB_TABLE_LENGTH;
    table->object[8]=phylib_new_hole(hole5Pos);
    free(hole5Pos);
    
    phylib_coord *hole6Pos=(phylib_coord *)calloc(1,sizeof(phylib_coord));
     if(hole6Pos==NULL){
        return NULL;
    }
    hole6Pos->x=PHYLIB_TABLE_WIDTH;
    hole6Pos->y=PHYLIB_TABLE_LENGTH;
    table->object[9]=phylib_new_hole(hole6Pos);
    free(hole6Pos);
    
    for(int i=10;i<PHYLIB_MAX_OBJECTS;i++){
        table->object[i]=NULL;
    }
    return table;
}

// Copies a phylib object from src to dest, allocating memory for the new object.
// If src is NULL, sets dest to NULL.
void phylib_copy_object(phylib_object **dest, phylib_object **src) {
    if (src == NULL || *src == NULL) {
        *dest = NULL;
        return;
    }

    *dest = (phylib_object *)calloc(1,sizeof(phylib_object));
    if (*dest != NULL) {
        memcpy(*dest, *src, sizeof(phylib_object));
    }else{
        return;
    }
}

// Creates a copy of a given table, including all objects within it.
// Returns a pointer to the copied table or NULL on allocation failure.
phylib_table *phylib_copy_table(phylib_table *table) {
    if (table == NULL) {
        return NULL;
    }

    phylib_table *new_table = (phylib_table *)calloc(1,sizeof(phylib_table));
    if (new_table == NULL) {
        return NULL; // Memory allocation failed
    }

    // Copy the primitive data members
    new_table->time = table->time;

    // Use phylib_copy_object to copy each object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object(&new_table->object[i], &table->object[i]);
        
    }

    return new_table;
}

// Adds an object to a table if there is a free spot in the table's array.
void phylib_add_object(phylib_table *table, phylib_object *object) {
    if (table == NULL || object == NULL) {
        return;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            return;
        }
    }

}

// Frees all memory associated with a table, including all objects within it.
void phylib_free_table(phylib_table *table) {
    if (table == NULL) {
        return;
    }
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
        }

    }

    free(table);
}

// Returns the difference between two coordinates as a new coordinate.
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord result;

    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
}

// Calculates the length of a coordinate vector using the Pythagorean theorem.
double phylib_length(phylib_coord c) {
    return sqrt((c.x * c.x) + (c.y * c.y));
}

// Computes the dot product of two coordinate vectors.
double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return ((a.x * b.x) + (a.y * b.y));
}

// Calculates the distance between two phylib objects. Returns -1.0 if obj1 is not a rolling ball or obj2 is an invalid type.
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }
    double distance;
    phylib_coord diff;

    switch (obj2->type) {
        case PHYLIB_STILL_BALL:
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
            distance = phylib_length(diff) - PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_ROLLING_BALL:
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            distance = phylib_length(diff) - PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_HOLE:
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            distance = phylib_length(diff) - PHYLIB_HOLE_RADIUS;
            break;

        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;

        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;

        default:
            return -1.0;
    }

    return distance;

}

// Updates the state of a rolling ball based on its velocity, acceleration, and elapsed time.
// If the ball's velocity changes sign, it is considered to have stopped.
void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }
    // Update positions according to the equations given
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + 
                                  (old->obj.rolling_ball.vel.x * time) + 
                                  (0.5 * old->obj.rolling_ball.acc.x * (time * time));

    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + 
                                  (old->obj.rolling_ball.vel.y * time) + 
                                  (0.5 * old->obj.rolling_ball.acc.y * (time * time));

    // Update velocities
    double new_vel_x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    double new_vel_y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    // Check for velocity sign change
    if ((old->obj.rolling_ball.vel.x < 0.0) == (new_vel_x < 0.0)) {
        new->obj.rolling_ball.vel.x = new_vel_x;
    } else {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((old->obj.rolling_ball.vel.y < 0.0) == (new_vel_y < 0.0)) {
        new->obj.rolling_ball.vel.y = new_vel_y;
    } else {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }

    
}


// Checks if a rolling ball has stopped. Converts it to a still ball if it has stopped.
// Returns 1 if conversion occurred, 0 otherwise.
unsigned char phylib_stopped(phylib_object *object) {
    if (object == NULL || object->type != PHYLIB_ROLLING_BALL) {
        return 0;
    }

    // Calculate the speed using the length of the velocity vector
    double speed = phylib_length(object->obj.rolling_ball.vel);

    // Check if the speed is less than the defined epsilon for a stop
    if (speed < PHYLIB_VEL_EPSILON) {
        // Convert to STILL_BALL
        object->type = PHYLIB_STILL_BALL;
        
        // Initialize the still ball with the position of the rolling ball and keep the number
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        

        // Reset velocity and acceleration
        object->obj.rolling_ball.vel.x = 0;
        object->obj.rolling_ball.vel.y = 0;
        object->obj.rolling_ball.acc.x = 0;
        object->obj.rolling_ball.acc.y = 0;

        return 1; // Conversion occurred
    }

    return 0; // No conversion occurred
}


// Handles the bounce behavior of a rolling ball when it collides with another object.
// The reaction depends on the type of the object being collided with.
void phylib_bounce(phylib_object **a, phylib_object **b) {
    if (a == NULL || *a == NULL || (*a)->type != PHYLIB_ROLLING_BALL) {
        return; // Object a is not a rolling ball or is NULL.
    }
    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            // Negate y velocity and y acceleration for a horizontal cushion
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;
        
        case PHYLIB_VCUSHION:
            // Negate x velocity and x acceleration for a vertical cushion
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;
        
        case PHYLIB_HOLE:
            // Free the memory of a and set it to NULL, representing the ball falling into a hole
            free(*a);
            *a = NULL;
            break;
        
        case PHYLIB_STILL_BALL:
            // Upgrade the still ball to a rolling ball and set initial velocity and acceleration
            (*b)->type = PHYLIB_ROLLING_BALL;
            // Fall through to the next case


        case PHYLIB_ROLLING_BALL:
            {
                // Calculate relative position vector r_ab
                phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

                // Calculate relative velocity vector v_rel
                phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

                // Compute normal vector n by normalizing r_ab
                double r_ab_length = phylib_length(r_ab);
                phylib_coord n = { r_ab.x / r_ab_length, r_ab.y / r_ab_length };

                // Compute relative velocity in the direction of n (v_rel_n)
                double v_rel_n = phylib_dot_product(v_rel, n);

                // Update vel of a and b
                (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
                (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);
                
                (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
                (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

                // Compute speeds of a and b
                double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
                double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

                // If the speed is greater than PHYLIB_VEL_EPSILON, update acceleration
                if (speed_a > PHYLIB_VEL_EPSILON) {
                    (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                    (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
                }
                if (speed_b > PHYLIB_VEL_EPSILON) {
                    (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
                }
            
            }
            break;
        default:
            // If b isn't a valid object type, do nothing
            break;
    }
}


// Counts the number of rolling balls on a table.
unsigned char phylib_rolling(phylib_table *t) {
    if (t == NULL) {
        return 0;
    }

    unsigned char count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count;
}
// Simulates a segment of motion on a pool table. Rolls each ball, checks for collisions, and handles stops or bounces.
// Returns a pointer to the updated table state.
phylib_table *phylib_segment(phylib_table *table) {
    if (table == NULL || phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *copy = phylib_copy_table(table);
    if (copy == NULL) {
        return NULL;
    }
    for (double currentTime = PHYLIB_SIM_RATE; currentTime <= PHYLIB_MAX_TIME; currentTime += PHYLIB_SIM_RATE) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL) {
                if(copy->object[i]==NULL){
                    phylib_free_table(copy); 
                    return NULL;
                }
                phylib_roll(copy->object[i],table->object[i], currentTime);
                if (phylib_stopped(copy->object[i])) {
                    copy->time = currentTime+table->time;
                    return copy;
                }
            }
        }


        for (int l = 0; l < PHYLIB_MAX_OBJECTS; l++) {
            if (copy->object[l] != NULL && copy->object[l]->type == PHYLIB_ROLLING_BALL) {

                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (l != j && copy->object[j] != NULL && phylib_distance(copy->object[l], copy->object[j]) < 0.0) {
                        phylib_bounce(&copy->object[l], &copy->object[j]);
                       
                        if (copy->object[l]) {
                            phylib_stopped(copy->object[l]);
                        }
                        copy->time = currentTime+table->time;
                        return copy;

                    }
                    
                }
            }
            
        }

        
        copy->time = currentTime+table->time;
    }
    return copy;
}

char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80,"NULL;");
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string,80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
            break;
        
        case PHYLIB_ROLLING_BALL:
            snprintf( string,80,
                    "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                    object->obj.rolling_ball.number,
                    object->obj.rolling_ball.pos.x,
                    object->obj.rolling_ball.pos.y,
                    object->obj.rolling_ball.vel.x,
                    object->obj.rolling_ball.vel.y,
                    object->obj.rolling_ball.acc.x,
                    object->obj.rolling_ball.acc.y );
            break;

        case PHYLIB_HOLE:
            snprintf( string,80,
                    "HOLE (%6.1lf,%6.1lf)",
                    object->obj.hole.pos.x,
                    object->obj.hole.pos.y );
            break;
        
        case PHYLIB_HCUSHION:
            snprintf( string,80,
                    "HCUSHION (%6.1lf)",
                    object->obj.hcushion.y );
            break;

        case PHYLIB_VCUSHION:
            snprintf( string,80,
                    "VCUSHION (%6.1lf)",
                    object->obj.vcushion.x );
            break;
    }
    return string;
}

